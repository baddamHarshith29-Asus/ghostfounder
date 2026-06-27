import React, { useState, useEffect, useRef } from 'react';

const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" 
  ? "http://localhost:5000/api" 
  : "/api";

function App() {
  // Navigation
  const [activeTab, setActiveTab] = useState("chat");
  const [userId, setUserId] = useState("founder_001");
  const [decisionCount, setDecisionCount] = useState(0);

  // API Config State
  const [config, setConfig] = useState({
    groqConfigured: false,
    hindsightConfigured: false,
    hindsightPipelineId: "",
    localModelUrl: "http://localhost:11434/v1",
    localModelName: "qwen"
  });
  const [showConfig, setShowConfig] = useState(false);
  const [groqKey, setGroqKey] = useState("");
  const [hindsightKey, setHindsightKey] = useState("");
  const [hindsightPipeline, setHindsightPipeline] = useState("");
  const [localUrl, setLocalUrl] = useState("http://localhost:11434/v1");
  const [localName, setLocalName] = useState("qwen");
  const [configMessage, setConfigMessage] = useState(null);

  // Strategy Chat State
  const [messages, setMessages] = useState([]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [recentConflict, setRecentConflict] = useState(null);
  const [memoryRecallActive, setMemoryRecallActive] = useState(false);
  const [recalledCount, setRecalledCount] = useState(0);

  // Debate State
  const [debateStage, setDebateStage] = useState("input"); // input, challenged, defended
  const [debateIdea, setDebateIdea] = useState("");
  const [debateCounterargs, setDebateCounterargs] = useState("");
  const [debateDefense, setDebateDefense] = useState("");
  const [debateVerdict, setDebateVerdict] = useState("");
  const [debateInitialScore, setDebateInitialScore] = useState(65);
  const [debateCurrentScore, setDebateCurrentScore] = useState(65);
  const [debateFeedback, setDebateFeedback] = useState("Awaiting your strategy to evaluate.");
  const [isDebateLoading, setIsDebateLoading] = useState(false);

  // History State
  const [history, setHistory] = useState([]);
  const [filterCat, setFilterCat] = useState("All");
  const [filterType, setFilterType] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [isHistoryLoading, setIsHistoryLoading] = useState(false);

  // Failure Pattern State
  const [failureSituation, setFailureSituation] = useState("");
  const [failureResults, setFailureResults] = useState(null);
  const [isFailureLoading, setIsFailureLoading] = useState(false);

  // Autopilot State
  const [autopilotTab, setAutopilotTab] = useState("brief"); // brief, competitor, email
  const [weeklyBrief, setWeeklyBrief] = useState(null);
  const [isBriefLoading, setIsBriefLoading] = useState(false);
  
  const [startupDesc, setStartupDesc] = useState("A collaborative task manager for software teams using AI.");
  const [competitorName, setCompetitorName] = useState("");
  const [competitorReport, setCompetitorReport] = useState(null);
  const [isCompetitorLoading, setIsCompetitorLoading] = useState(false);

  const [customerEmail, setCustomerEmail] = useState("Your product is too expensive for small teams. Can we get a 50% discount?");
  const [emailDraft, setEmailDraft] = useState(null);
  const [isEmailLoading, setIsEmailLoading] = useState(false);
  const [emailMeta, setEmailMeta] = useState(null);

  // Routing Dashboard State
  const [routingLog, setRoutingLog] = useState([]);
  const [routingStats, setRoutingStats] = useState({
    total: 0,
    fast: 0,
    power: 0,
    avgLatency: 0,
    totalCost: 0,
    staticCost: 0,
    saved: 0,
    savedPct: 0
  });

  // Mood Detector State
  const [moodTimeline, setMoodTimeline] = useState(null);
  const [currentMood, setCurrentMood] = useState(null);
  const [isMoodLoading, setIsMoodLoading] = useState(false);

  // Graveyard State
  const [graveyardStrategy, setGraveyardStrategy] = useState("");
  const [graveyardResults, setGraveyardResults] = useState(null);
  const [isGraveyardLoading, setIsGraveyardLoading] = useState(false);

  // Flip-Flop Score State
  const [flipflopData, setFlipflopData] = useState(null);

  const chatEndRef = useRef(null);

  // ── Lifecycles & Syncs ──────────────────────────────────────

  useEffect(() => {
    // Initial fetch of configuration and dashboard logs
    fetchConfig();
    fetchStats();
    fetchRoutingLogs();
    fetchFlipflopScore();
    fetchMoodTimeline();
  }, []);

  useEffect(() => {
    // Auto-scroll chat window when new message arrives
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isChatLoading]);

  useEffect(() => {
    if (activeTab === "history") {
      loadHistory();
    } else if (activeTab === "routing") {
      fetchRoutingLogs();
    } else if (activeTab === "mood") {
      fetchMoodTimeline();
    }
  }, [activeTab, filterCat, filterType, searchQuery]);

  // ── API Fetch Functions ─────────────────────────────────────

  const fetchConfig = async () => {
    try {
      const res = await fetch(`${API_BASE}/config`);
      const data = await res.json();
      setConfig(data);
      if (data.hindsightPipelineId) {
        setHindsightPipeline(data.hindsightPipelineId);
      }
      if (data.localModelUrl) {
        setLocalUrl(data.localModelUrl);
      }
      if (data.localModelName) {
        setLocalName(data.localModelName);
      }
    } catch (err) {
      console.error("Error loading API config: ", err);
    }
  };

  const saveConfig = async (e) => {
    e.preventDefault();
    setConfigMessage({ type: "info", text: "Updating keys..." });
    try {
      const res = await fetch(`${API_BASE}/config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          groqKey: groqKey,
          hindsightKey: hindsightKey,
          hindsightPipelineId: hindsightPipeline,
          localModelUrl: localUrl,
          localModelName: localName
        })
      });
      const data = await res.json();
      if (data.status === "success") {
        setConfigMessage({ type: "success", text: "Keys updated!" });
        fetchConfig();
        // Clear forms
        setGroqKey("");
        setHindsightKey("");
      } else {
        setConfigMessage({ type: "error", text: "Error saving keys." });
      }
    } catch (err) {
      setConfigMessage({ type: "error", text: "Connection error." });
    }
    setTimeout(() => setConfigMessage(null), 3000);
  };

  const fetchStats = async () => {
    try {
      const res = await fetch(`${API_BASE}/history?userId=${userId}`);
      const data = await res.json();
      setDecisionCount(data.totalCount || 0);
    } catch (err) {
      console.error("Error loading stats: ", err);
    }
  };

  const loadHistory = async () => {
    setIsHistoryLoading(true);
    try {
      const res = await fetch(`${API_BASE}/history?userId=${userId}&category=${filterCat}&type=${filterType}`);
      const data = await res.json();
      let list = data.history || [];
      if (searchQuery) {
        list = list.filter(item => item.content.toLowerCase().includes(searchQuery.toLowerCase()));
      }
      setHistory(list);
    } catch (err) {
      console.error("Error loading history: ", err);
    } finally {
      setIsHistoryLoading(false);
    }
  };

  const resetAll = async () => {
    if (window.confirm("Are you sure you want to clear all memory and logs? This resets the demo.")) {
      try {
        await fetch(`${API_BASE}/history/clear`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId: userId })
        });
        setMessages([]);
        setDecisionCount(0);
        setRecentConflict(null);
        setRoutingLog([]);
        setHistory([]);
        alert("System reset completed!");
        fetchStats();
        fetchRoutingLogs();
      } catch (err) {
        alert("Error resetting server data.");
      }
    }
  };

  const fetchRoutingLogs = async () => {
    try {
      const res = await fetch(`${API_BASE}/routing/log`);
      const data = await res.json();
      const logs = data.log || [];
      setRoutingLog(logs);

      // Compute statistics
      if (logs.length > 0) {
        const total = logs.length;
        const fast = logs.filter(r => r.model.includes("8b")).length;
        const power = logs.filter(r => r.model.includes("70b")).length;
        const avgLatency = Math.round(logs.reduce((acc, r) => acc + r.latency_ms, 0) / total);
        const totalCost = logs.reduce((acc, r) => acc + (r.cost || 0), 0);
        const staticCost = logs.reduce((acc, r) => acc + (r.static_cost || 0), 0);
        const saved = logs.reduce((acc, r) => acc + (r.cost_saved || 0), 0);
        const savedPct = staticCost > 0 ? Math.round((saved / staticCost) * 100) : 0;
        
        setRoutingStats({
          total, fast, power, avgLatency, totalCost, staticCost, saved, savedPct
        });
      } else {
        // Mock fallback statistics for empty state
        setRoutingStats({
          total: 5, fast: 2, power: 3, avgLatency: 664, totalCost: 0.00127, staticCost: 0.00143, saved: 0.00016, savedPct: 11
        });
      }
    } catch (err) {
      console.error("Error loading routing logs: ", err);
    }
  };

  // ── Mood & Graveyard & Flipflop Fetch Functions ──────────────

  const fetchMoodTimeline = async () => {
    try {
      const res = await fetch(`${API_BASE}/mood/timeline?userId=${userId}`);
      const data = await res.json();
      setMoodTimeline(data);
      if (data.currentMood) {
        setCurrentMood(data);
      }
    } catch (err) {
      console.error("Error loading mood timeline:", err);
    }
  };

  const compareToGraveyard = async () => {
    if (!graveyardStrategy.trim()) return;
    setIsGraveyardLoading(true);
    setGraveyardResults(null);
    try {
      const res = await fetch(`${API_BASE}/graveyard/compare`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ strategy: graveyardStrategy })
      });
      const data = await res.json();
      setGraveyardResults(data);
    } catch (err) {
      alert("Graveyard comparison error.");
    } finally {
      setIsGraveyardLoading(false);
    }
  };

  const fetchFlipflopScore = async () => {
    try {
      const res = await fetch(`${API_BASE}/flipflop/score?userId=${userId}`);
      const data = await res.json();
      setFlipflopData(data);
    } catch (err) {
      console.error("Error loading flipflop score:", err);
    }
  };

  // ── Strategy Chat Functions ──────────────────────────────────

  const handleSendMessage = async (textToSend) => {
    const input = textToSend || chatInput;
    if (!input.trim()) return;

    setChatInput("");
    setRecentConflict(null);
    setMemoryRecallActive(false);

    // Append user message
    const userMsg = { role: "user", content: input };
    setMessages(prev => [...prev, userMsg]);
    setIsChatLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, message: input })
      });
      const data = await res.json();

      if (data.conflict) {
        setRecentConflict(data.conflict);
      }
      if (data.memories && data.memories.length > 0) {
        setMemoryRecallActive(true);
        setRecalledCount(data.memories.length);
      }
      // Capture mood from response
      if (data.mood) {
        setCurrentMood(prev => ({
          ...prev,
          currentMood: data.mood,
          currentMoodKey: data.mood.mood
        }));
      }

      // Append assistant message
      const assistantMsg = {
        role: "assistant",
        content: data.response,
        model: data.model,
        tier: data.tier,
        latency: data.latency,
        mood: data.mood
      };
      setMessages(prev => [...prev, assistantMsg]);
      fetchStats();
      fetchRoutingLogs();
      fetchFlipflopScore();
      fetchMoodTimeline();
    } catch (err) {
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "API connection error. Make sure server.py is running on port 5000."
      }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  const handleShortcutClick = async (type) => {
    // Seed backend memory for relevant scenarios, then submit chat query
    if (type === "discount") {
      // Seed first
      try {
        await fetch(`${API_BASE}/history/clear`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId: userId })
        });
      } catch (e) {}

      // Seed pricing decision
      await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: userId,
          message: "On February 14th, I committed that we will never compete on price or run discount campaigns. Discounting attracts transactional customers with high support needs. In January, a price campaign cost us ₹25,000 in refunds."
        })
      });
      handleSendMessage("I'm thinking about running a 50% discount campaign this weekend to quickly boost customer volume. What do you think?");
    } 
    else if (type === "features") {
      try {
        await fetch(`${API_BASE}/history/clear`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId: userId })
        });
      } catch (e) {}

      await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId: userId,
          message: "On March 3rd, we decided to restrict product development. We will focus purely on one core dashboard view and refuse to build additional features until we reach 100 paid users."
        })
      });
      handleSendMessage("Let's build 5 new features this sprint (Slack alerts, custom export, team subaccounts, analytics tab, and calendar sync) so we can appeal to more customers.");
    } 
    else if (type === "routing") {
      handleSendMessage("Should I seek venture capital funding or bootstrap my startup?");
    }
  };

  // ── Co-Founder Debate Functions ──────────────────────────────

  const handleDebateShortcut = (ideaType) => {
    setDebateStage("input");
    setDebateDefense("");
    setDebateVerdict("");
    if (ideaType === "freemium") {
      setDebateIdea("I want to launch a 100% free tier of our product to drive viral acquisition, hoping they convert later.");
    } else if (ideaType === "rebuild") {
      setDebateIdea("I want to spend 2 months refactoring the database and rebuilding the front-end codebase from scratch to make it faster.");
    } else if (ideaType === "hiring") {
      setDebateIdea("I want to hire 3 engineers and 2 sales reps immediately using credit lines to capture market share.");
    }
  };

  const submitDebateStrategy = async () => {
    if (!debateIdea.trim()) return;
    setIsDebateLoading(true);
    try {
      const res = await fetch(`${API_BASE}/debate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, idea: debateIdea })
      });
      const data = await res.json();
      setDebateCounterargs(data.counterargs);
      setDebateInitialScore(data.initialScore);
      setDebateCurrentScore(data.currentScore);
      setDebateFeedback(data.feedback);
      setDebateStage("challenged");
    } catch (err) {
      alert("Debate error. Check server status.");
    } finally {
      setIsDebateLoading(false);
    }
  };

  const submitDebateDefense = async () => {
    if (!debateDefense.trim()) return;
    setIsDebateLoading(true);
    try {
      const res = await fetch(`${API_BASE}/debate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          userId,
          idea: debateIdea,
          counterargs: debateCounterargs,
          defense: debateDefense
        })
      });
      const data = await res.json();
      setDebateVerdict(data.verdict);
      setDebateCurrentScore(data.currentScore);
      setDebateFeedback(data.feedback);
      setDebateStage("defended");
      fetchStats();
    } catch (err) {
      alert("Debate evaluation error.");
    } finally {
      setIsDebateLoading(false);
    }
  };

  // ── Failure Patterns Scanner Functions ─────────────────────────

  const handleFailureShortcut = (planType) => {
    if (planType === "pricing") {
      setFailureSituation("We want to launch next week by undercutting our major competitors by 50% and running heavy discounts. We will acquire their users fast.");
    } else if (planType === "features") {
      setFailureSituation("We are going to hold the launch for another month so that we can build Slack alerts, dashboard export, sub-accounts, and 5 other features to satisfy every customer.");
    } else if (planType === "burn") {
      setFailureSituation("We plan to raise our burn rate by hiring 3 developers and renting a workspace before we lock in our retention. We need to grow fast.");
    }
  };

  const scanStrategyForFailures = async () => {
    if (!failureSituation.trim()) return;
    setIsFailureLoading(true);
    setFailureResults(null);
    try {
      const res = await fetch(`${API_BASE}/failure`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ situation: failureSituation })
      });
      const data = await res.json();
      setFailureResults(data.patterns || []);
    } catch (err) {
      alert("Error scanning strategy.");
    } finally {
      setIsFailureLoading(false);
    }
  };

  // ── Autopilot Functions ──────────────────────────────────────

  const generateAutopilotBrief = async () => {
    setIsBriefLoading(true);
    setWeeklyBrief(null);
    try {
      const res = await fetch(`${API_BASE}/autopilot/brief?userId=${userId}`);
      const data = await res.json();
      if (data.status === "success") {
        setWeeklyBrief(data);
        fetchStats();
      } else {
        setWeeklyBrief({ brief: data.message || "No history yet. Start chatting to build memory." });
      }
    } catch (err) {
      alert("Autopilot connection error.");
    } finally {
      setIsBriefLoading(false);
    }
  };

  const getCompetitorIntelligence = async () => {
    if (!competitorName.trim()) return;
    setIsCompetitorLoading(true);
    setCompetitorReport(null);
    try {
      const res = await fetch(`${API_BASE}/autopilot/competitor`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: startupDesc, competitorName })
      });
      const data = await res.json();
      setCompetitorReport(data.report);
    } catch (err) {
      alert("Surveillance compilation failed.");
    } finally {
      setIsCompetitorLoading(false);
    }
  };

  const runDraftResponse = async () => {
    if (!customerEmail.trim()) return;
    setIsEmailLoading(true);
    setEmailDraft(null);
    try {
      const res = await fetch(`${API_BASE}/autopilot/email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, emailText: customerEmail })
      });
      const data = await res.json();
      setEmailDraft(data.reply);
      setEmailMeta({ model: data.model, latency: data.latency });
    } catch (err) {
      alert("Draft execution failed.");
    } finally {
      setIsEmailLoading(false);
    }
  };

  // ── Score Colors ────────────────────────────────────────────

  const getScoreColor = (s) => {
    if (s > 75) return "green";
    if (s > 50) return "amber";
    return "red";
  };

  // ── Render Helpers ──────────────────────────────────────────

  const renderConfigMessage = () => {
    if (!configMessage) return null;
    return (
      <div style={{
        padding: '8px', 
        fontSize: '11px', 
        borderRadius: '4px',
        backgroundColor: configMessage.type === 'success' ? '#064e3b' : configMessage.type === 'error' ? '#7f1d1d' : '#1e1b4b',
        color: 'white',
        marginTop: '8px',
        textAlign: 'center'
      }}>
        {configMessage.text}
      </div>
    );
  };

  return (
    <div className="app-container">
      {/* ── SIDEBAR ── */}
      <div className="sidebar">
        <div className="logo-container">
          <h2 className="logo-title">👻 GHOST FOUNDER</h2>
          <p className="logo-sub">The Co-Founder that never forgets</p>
        </div>

        <div className="stats-card-mini">
          <p className="stats-label">Decisions Remembered</p>
          <p className="stats-value">{decisionCount}</p>
        </div>

        <div className="nav-menu">
          <div className={`nav-item ${activeTab === "chat" ? "active" : ""}`} onClick={() => setActiveTab("chat")}>
            <span className="nav-item-icon">💬</span> Strategy Chat
          </div>
          <div className={`nav-item ${activeTab === "debate" ? "active" : ""}`} onClick={() => setActiveTab("debate")}>
            <span className="nav-item-icon">⚔️</span> Co-Founder Debate
          </div>
          <div className={`nav-item ${activeTab === "history" ? "active" : ""}`} onClick={() => setActiveTab("history")}>
            <span className="nav-item-icon">📊</span> Decision History
          </div>
          <div className={`nav-item ${activeTab === "failures" ? "active" : ""}`} onClick={() => setActiveTab("failures")}>
            <span className="nav-item-icon">⚠️</span> Failure Patterns
          </div>
          <div className={`nav-item ${activeTab === "autopilot" ? "active" : ""}`} onClick={() => setActiveTab("autopilot")}>
            <span className="nav-item-icon">🤖</span> Autopilot Suite
          </div>
          <div className={`nav-item ${activeTab === "routing" ? "active" : ""}`} onClick={() => setActiveTab("routing")}>
            <span className="nav-item-icon">⚡</span> Routing Dashboard
          </div>
          <div className={`nav-item ${activeTab === "mood" ? "active" : ""}`} onClick={() => setActiveTab("mood")}>
            <span className="nav-item-icon">🧠</span> Founder Pulse
          </div>
          <div className={`nav-item ${activeTab === "graveyard" ? "active" : ""}`} onClick={() => setActiveTab("graveyard")}>
            <span className="nav-item-icon">💀</span> Startup Graveyard
          </div>
        </div>

        {/* Flip-Flop Consistency Score Card */}
        {flipflopData && (
          <div className="flipflop-sidebar-card">
            <div className="flipflop-score-display" style={{ color: flipflopData.gradeColor }}>
              {flipflopData.score}
            </div>
            <div className="flipflop-grade" style={{ color: flipflopData.gradeColor }}>
              {flipflopData.grade} — {flipflopData.gradeLabel}
            </div>
            <div className="flipflop-label">Strategic Consistency</div>
            {flipflopData.streakDays > 0 && (
              <div className="flipflop-streak">
                🔥 {flipflopData.streakDays}d streak
              </div>
            )}
            {flipflopData.totalReversals > 0 && (
              <div style={{ fontSize: '10px', color: '#f59e0b', marginTop: '4px' }}>
                🔄 {flipflopData.totalReversals} reversal{flipflopData.totalReversals > 1 ? 's' : ''} detected
              </div>
            )}
          </div>
        )}

        <div className="sidebar-divider"></div>

        {/* API CONFIG EXPANDER */}
        <div className="config-header" onClick={() => setShowConfig(!showConfig)}>
          <span>⚙️ API Keys Manager</span>
          <span>{showConfig ? "▲" : "▼"}</span>
        </div>
        
        {showConfig && (
          <form className="config-form" onSubmit={saveConfig}>
            <div className="input-group">
              <span className="input-label">Groq API Key</span>
              <input 
                type="password" 
                className="input-field"
                placeholder={config.groqConfigured ? "••••••••••••••••" : "Add Groq key"} 
                value={groqKey}
                onChange={e => setGroqKey(e.target.value)}
              />
            </div>
            <div className="input-group">
              <span className="input-label">Hindsight API Key</span>
              <input 
                type="password" 
                className="input-field"
                placeholder={config.hindsightConfigured ? "••••••••••••••••" : "Add Hindsight key"} 
                value={hindsightKey}
                onChange={e => setHindsightKey(e.target.value)}
              />
            </div>
            <div className="input-group">
              <span className="input-label">Hindsight Pipeline ID</span>
              <input 
                type="text" 
                className="input-field"
                placeholder="Pipeline ID" 
                value={hindsightPipeline}
                onChange={e => setHindsightPipeline(e.target.value)}
              />
            </div>
            <div className="input-group">
              <span className="input-label">Local Qwen Model URL</span>
              <input 
                type="text" 
                className="input-field"
                placeholder="http://localhost:11434/v1" 
                value={localUrl}
                onChange={e => setLocalUrl(e.target.value)}
              />
            </div>
            <div className="input-group">
              <span className="input-label">Local Qwen Model Name</span>
              <input 
                type="text" 
                className="input-field"
                placeholder="qwen" 
                value={localName}
                onChange={e => setLocalName(e.target.value)}
              />
            </div>
            <button type="submit" className="btn-primary">Save Configuration</button>
            {renderConfigMessage()}
          </form>
        )}

        <div className="sidebar-reset-container">
          <button className="btn-reset" onClick={resetAll}>🧹 Clear Data</button>
          <button className="btn-reset" onClick={fetchRoutingLogs}>⚡ Sync Logs</button>
        </div>
      </div>

      {/* ── MAIN CONTENT AREA ── */}
      <div className="main-content">
        
        {/* 💬 Strategy Chat Tab */}
        {activeTab === "chat" && (
          <div>
            <h1 className="page-title">💬 Strategy Chat</h1>
            <p className="page-subtitle">Formulate startup logic. Ghost Founder pulls memories, matches conflicts, and routes query streams dynamically.</p>
            
            {!config.groqConfigured && (
              <div className="conflict-alert" style={{ background: "rgba(124, 58, 237, 0.05)", borderColor: "rgba(124, 58, 237, 0.2)", color: "#c084fc", animation: "none" }}>
                📢 <strong>Demo Simulation Mode:</strong> App is running offline using local mocks. Insert your Groq API Key to test live LLM generation.
              </div>
            )}

            {/* Quick Presets */}
            <div className="demo-shortcuts">
              <h5 className="shortcut-title">🚀 Demo Shortcuts (1-Click Judge Actions)</h5>
              <div className="shortcut-grid">
                <div className="shortcut-card" onClick={() => handleShortcutClick("discount")}>
                  <div className="shortcut-name">🛑 Pricing Contradiction</div>
                  <div className="shortcut-desc">Decision Feb 14: Never discount. Trigger discount proposal to test conflict alarm.</div>
                </div>
                <div className="shortcut-card" onClick={() => handleShortcutClick("features")}>
                  <div className="shortcut-name">🛠️ Feature Overload</div>
                  <div className="shortcut-desc">Decision Mar 3: Focus on 1 feature. Try proposing 5 features to check focus contradiction.</div>
                </div>
                <div className="shortcut-card" onClick={() => handleShortcutClick("routing")}>
                  <div className="shortcut-name">📈 Complex Question Routing</div>
                  <div className="shortcut-desc">Ask "Bootstrap vs Funding" to trigger automatic routing to Llama3-70B model.</div>
                </div>
              </div>
            </div>

            {/* Warning Banners */}
            {recentConflict && (
              <div className="conflict-alert">
                <strong>🚨 STRATEGIC CONTRADICTION DETECTED</strong><br />
                {recentConflict}
              </div>
            )}

            {memoryRecallActive && (
              <div className="memory-alert">
                <strong>🧠 HINDSIGHT MEMORY RETRIEVAL</strong><br />
                Retrieved {recalledCount} past decisions/contexts. Factoring these into the strategy.
              </div>
            )}

            {/* Chat Box */}
            <div className="glass-card">
              <div className="chat-window">
                {messages.length === 0 ? (
                  <div className="chat-welcome">
                    <div className="chat-welcome-icon">👻</div>
                    <strong>Ghost Founder is active.</strong><br />
                    Try pitching a pricing discount or ask: <em>"Should I hire devs now or bootstrap?"</em>
                  </div>
                ) : (
                  messages.map((m, idx) => (
                    <div key={idx} className={`chat-bubble ${m.role}`}>
                      <div className={`chat-avatar ${m.role}`}>
                        {m.role === 'user' ? 'ME' : 'GF'}
                      </div>
                      <div className="chat-bubble-content">
                        <div>{m.content}</div>
                        {m.role === 'assistant' && m.model && (
                          <div className="meta-row">
                            <span className={`badge ${m.model.includes('8b') ? 'green' : 'purple'}`}>
                              🤖 {m.model}
                            </span>
                            <span className="meta-text">
                              ⏱️ {m.latency}ms | 💸 Tier: {m.tier}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))
                )}
                {isChatLoading && (
                  <div className="chat-bubble assistant">
                    <div className="chat-avatar assistant">GF</div>
                    <div className="chat-bubble-content">
                      <div style={{ fontStyle: 'italic', color: '#64748b' }}>Ghost Founder is thinking...</div>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Chat Input */}
              <div className="chat-input-container">
                <input 
                  type="text" 
                  className="chat-input-field" 
                  placeholder="Ask your co-founder anything..."
                  value={chatInput}
                  onChange={e => setChatInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                  disabled={isChatLoading}
                />
                <button 
                  className="btn-primary" 
                  onClick={() => handleSendMessage()}
                  disabled={isChatLoading}
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ⚔️ Co-Founder Debate Tab */}
        {activeTab === "debate" && (
          <div>
            <h1 className="page-title">⚔️ Co-Founder Debate Arena</h1>
            <p className="page-subtitle">Pitch a strategy. The co-founder will tear it down. Defend your case to score viability points.</p>

            <div className="demo-shortcuts">
              <h5 className="shortcut-title">🥊 Select a Strategy to Debate:</h5>
              <div className="shortcut-grid">
                <div className="shortcut-card" style={{ borderColor: 'rgba(239,68,68,0.2)' }} onClick={() => handleDebateShortcut("freemium")}>
                  <div className="shortcut-name" style={{ color: '#f43f5e' }}>📉 Freemium Funnel</div>
                  <div className="shortcut-desc">Launch a free tier for viral signups without conversion triggers.</div>
                </div>
                <div className="shortcut-card" style={{ borderColor: 'rgba(239,68,68,0.2)' }} onClick={() => handleDebateShortcut("rebuild")}>
                  <div className="shortcut-name" style={{ color: '#f43f5e' }}>🛠️ Codebase Rebuild</div>
                  <div className="shortcut-desc">Halt launch for 2 months to refactor database models and backend structure.</div>
                </div>
                <div className="shortcut-card" style={{ borderColor: 'rgba(239,68,68,0.2)' }} onClick={() => handleDebateShortcut("hiring")}>
                  <div className="shortcut-name" style={{ color: '#f43f5e' }}>👥 Headcount Inflation</div>
                  <div className="shortcut-desc">Hire 3 engineers and 2 reps on credit lines to capture market share immediately.</div>
                </div>
              </div>
            </div>

            <div className="debate-grid">
              {/* Left Panel: Sparring Ring */}
              <div className="glass-card">
                {debateStage === "input" && (
                  <div>
                    <h3 style={{ marginBottom: '16px' }}>🥊 State Your Strategy</h3>
                    <textarea 
                      className="input-field" 
                      style={{ width: '100%', minHeight: '120px', resize: 'none', marginBottom: '16px' }}
                      placeholder="Explain your strategic plan. e.g. I want to offer 50% discounts to grow user volume..."
                      value={debateIdea}
                      onChange={e => setDebateIdea(e.target.value)}
                    />
                    <button 
                      className="btn-primary" 
                      style={{ width: '100%' }}
                      onClick={submitDebateStrategy}
                      disabled={isDebateLoading}
                    >
                      {isDebateLoading ? "Generating Counterarguments..." : "🥊 Challenge Strategy"}
                    </button>
                  </div>
                )}

                {debateStage === "challenged" && (
                  <div>
                    <h4 style={{ color: '#cbd5e1', marginBottom: '12px' }}>Your Strategy:</h4>
                    <p style={{ fontStyle: 'italic', color: '#a78bfa', marginBottom: '20px' }}>"{debateIdea}"</p>
                    
                    <h4 style={{ color: '#f43f5e', marginBottom: '12px' }}>❌ Challenger's Counterarguments:</h4>
                    <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: '#fda4af', background: 'rgba(244,63,94,0.03)', border: '1px solid rgba(244,63,94,0.1)', padding: '16px', borderRadius: '8px', marginBottom: '20px' }}>
                      {debateCounterargs}
                    </div>

                    <h4 style={{ marginBottom: '12px' }}>🛡️ Defend Your Strategy</h4>
                    <textarea 
                      className="input-field"
                      style={{ width: '100%', minHeight: '100px', resize: 'none', marginBottom: '16px' }}
                      placeholder="Back up your logic: include metrics, scoping limits, or MVP tests..."
                      value={debateDefense}
                      onChange={e => setDebateDefense(e.target.value)}
                    />
                    
                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                      <button 
                        className="btn-primary"
                        onClick={submitDebateDefense}
                        disabled={isDebateLoading}
                      >
                        {isDebateLoading ? "Evaluating Defense..." : "🛡️ Defend Strategy"}
                      </button>
                      <button 
                        className="btn-secondary"
                        onClick={() => setDebateStage("input")}
                      >
                        🔄 Reset Ring
                      </button>
                    </div>
                  </div>
                )}

                {debateStage === "defended" && (
                  <div>
                    <h4 style={{ color: '#cbd5e1', marginBottom: '12px' }}>Your Strategy:</h4>
                    <p style={{ fontStyle: 'italic', color: '#94a3b8', marginBottom: '16px' }}>"{debateIdea}"</p>

                    <h4 style={{ color: '#10b981', marginBottom: '12px' }}>⚖️ Co-Founder's Final Verdict:</h4>
                    <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', color: '#a7f3d0', background: 'rgba(16,185,129,0.03)', border: '1px solid rgba(16,185,129,0.1)', padding: '16px', borderRadius: '8px', marginBottom: '24px' }}>
                      {debateVerdict}
                    </div>

                    <button 
                      className="btn-primary" 
                      style={{ width: '100%' }}
                      onClick={() => handleDebateShortcut("")}
                    >
                      🔄 Start New Debate
                    </button>
                  </div>
                )}
              </div>

              {/* Right Panel: Scorecard */}
              <div className="glass-card viability-index-card">
                <p style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.05em' }}>VIABILITY REPORT CARD</p>
                
                {debateStage === "input" ? (
                  <div style={{ padding: '40px 0', color: 'var(--text-muted)', fontSize: '13px' }}>
                    Enter strategy pitch to activate score tracking metrics.
                  </div>
                ) : (
                  <div style={{ width: '100%' }}>
                    <div className={`viability-number ${getScoreColor(debateCurrentScore)}`}>
                      {debateCurrentScore}
                      <span style={{ fontSize: '18px', color: 'var(--text-muted)' }}> / 100</span>
                    </div>

                    <div className={`viability-delta ${debateCurrentScore >= debateInitialScore ? "up" : "down"}`}>
                      {debateCurrentScore >= debateInitialScore 
                        ? `▲ Defense improved viability by +${debateCurrentScore - debateInitialScore} pts`
                        : `▼ Verdict dropped viability by ${debateCurrentScore - debateInitialScore} pts`
                      }
                    </div>

                    <div className="viability-progress">
                      <div 
                        className={`viability-bar ${getScoreColor(debateCurrentScore)}`}
                        style={{ width: `${debateCurrentScore}%` }}
                      ></div>
                    </div>

                    <div style={{ background: '#13131f', border: '1px solid #1e1e2d', padding: '16px', borderRadius: '8px', textAlign: 'left', marginTop: '20px' }}>
                      <span style={{ fontSize: '11px', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Strategy evaluation:</span>
                      <p style={{ fontSize: '12px', marginTop: '6px', color: '#cbd5e1', lineHeight: '1.4' }}>{debateFeedback}</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* 📊 Decision History Tab */}
        {activeTab === "history" && (
          <div>
            <h1 className="page-title">📊 Decision History</h1>
            <p className="page-subtitle">A chronological record of every decision you have committed to, categorized by topic.</p>

            <div className="glass-card filter-bar">
              <div className="input-group">
                <span className="input-label">Search Decisions</span>
                <input 
                  type="text" 
                  className="input-field" 
                  placeholder="Filter keywords..."
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                />
              </div>
              <div className="input-group">
                <span className="input-label">Startup Category</span>
                <select 
                  className="input-field"
                  value={filterCat}
                  onChange={e => setFilterCat(e.target.value)}
                >
                  <option value="All">All Categories</option>
                  <option value="Pricing">Pricing</option>
                  <option value="Product">Product</option>
                  <option value="Marketing">Marketing</option>
                  <option value="Finance">Finance</option>
                  <option value="Team">Team</option>
                  <option value="General">General</option>
                </select>
              </div>
              <div className="input-group">
                <span className="input-label">Log Type</span>
                <select 
                  className="input-field"
                  value={filterType}
                  onChange={e => setFilterType(e.target.value)}
                >
                  <option value="All">All Types</option>
                  <option value="decision">Decision</option>
                  <option value="chat">Chat Log</option>
                  <option value="debate">Debate Outcome</option>
                </select>
              </div>
            </div>

            {isHistoryLoading ? (
              <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>Loading history logs...</div>
            ) : history.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>No matching entries found. Go add decisions in Strategy Chat!</div>
            ) : (
              <div>
                {/* SVG Visual Timeline */}
                {history.length >= 2 && (
                  <div className="glass-card" style={{ padding: '16px' }}>
                    <h4 style={{ marginBottom: '12px', fontSize: '13px' }}>Historical Decision Milestones</h4>
                    <div style={{ display: 'flex', alignItems: 'center', width: '100%', overflowX: 'auto', padding: '20px 0' }}>
                      <svg width="100%" height="80" style={{ minWidth: '600px' }}>
                        {/* Timeline horizontal axis */}
                        <line x1="40" y1="40" x2="95%" y2="40" stroke="#1f1f2e" strokeWidth="4" />
                        
                        {/* Nodes */}
                        {history.map((item, idx) => {
                          const percent = 40 + (idx / (history.length - 1)) * 500;
                          return (
                            <g key={idx}>
                              <circle 
                                cx={`${5 + (idx / (history.length - 1)) * 90}%`} 
                                cy="40" 
                                r="8" 
                                fill={item.category === "Pricing" ? "#d97706" : item.category === "Product" ? "#7c3aed" : "#10b981"}
                                stroke="white"
                                strokeWidth="2"
                              />
                              <text 
                                x={`${5 + (idx / (history.length - 1)) * 90}%`} 
                                y="20" 
                                fill="#94a3b8" 
                                fontSize="9" 
                                textAnchor="middle"
                              >
                                {item.category}
                              </text>
                              <text 
                                x={`${5 + (idx / (history.length - 1)) * 90}%`} 
                                y="65" 
                                fill="#cbd5e1" 
                                fontSize="8" 
                                textAnchor="middle"
                              >
                                {item.content.substring(0, 12)}...
                              </text>
                            </g>
                          );
                        })}
                      </svg>
                    </div>
                  </div>
                )}

                {/* List Feed */}
                {history.map((item, idx) => (
                  <div key={idx} className="glass-card">
                    <div className="history-card-header">
                      <div>
                        <span className={`badge ${
                          item.category === "Pricing" ? "amber" : item.category === "Product" ? "purple" : "green"
                        }`}>
                          {item.category || "General"}
                        </span>
                        <span style={{ background: 'rgba(255,255,255,0.03)', color: 'var(--text-muted)', fontSize: '10px', padding: '2px 8px', borderRadius: '4px', marginLeft: '8px' }}>
                          type: {item.type}
                        </span>
                        {item.hindsight_stored && (
                          <span style={{ color: '#10b981', fontSize: '11px', marginLeft: '12px' }}>✓ Synced Pipeline</span>
                        )}
                      </div>
                      <span style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
                        {item.timestamp ? new Date(item.timestamp).toLocaleString() : ""}
                      </span>
                    </div>
                    <div className="history-card-body">{item.content}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ⚠️ Failure Patterns Tab */}
        {activeTab === "failures" && (
          <div>
            <h1 className="page-title">⚠️ Failure Pattern Scanner</h1>
            <p className="page-subtitle">Evaluate strategy vectors against danger zones built from historical startup crash logs.</p>

            <div className="demo-shortcuts">
              <h5 className="shortcut-title">🚀 Click to Test Common Failure Scenarios:</h5>
              <div className="shortcut-grid">
                <div className="shortcut-card" onClick={() => handleFailureShortcut("pricing")}>
                  <div className="shortcut-name">🏷️ Pricing undercut race</div>
                  <div className="shortcut-desc">Cut margins in half and run discount campaigns.</div>
                </div>
                <div className="shortcut-card" onClick={() => handleFailureShortcut("features")}>
                  <div className="shortcut-name">💻 Holding launch for features</div>
                  <div className="shortcut-desc">Freeze launch for 3 sprints to construct 5 more integrations.</div>
                </div>
                <div className="shortcut-card" onClick={() => handleFailureShortcut("burn")}>
                  <div className="shortcut-name">💰 Premature growth hire</div>
                  <div className="shortcut-desc">Hire 3 dev and sales agents before reaching retention PMF.</div>
                </div>
              </div>
            </div>

            <div className="glass-card">
              <h3 style={{ marginBottom: '16px' }}>🔍 Scan Plan</h3>
              <textarea 
                className="input-field" 
                style={{ width: '100%', minHeight: '120px', resize: 'none', marginBottom: '16px' }}
                placeholder="Detail your strategy. e.g. We are building 10 features to capture multiple customer sectors..."
                value={failureSituation}
                onChange={e => setFailureSituation(e.target.value)}
              />
              <button 
                className="btn-primary" 
                style={{ width: '100%' }}
                onClick={scanStrategyForFailures}
                disabled={isFailureLoading}
              >
                {isFailureLoading ? "Scanning Startup Database..." : "🔍 Check for Failure Patterns"}
              </button>
            </div>

            {failureResults !== null && (
              <div>
                <h3 style={{ marginBottom: '16px' }}>Scan Report ({failureResults.length} Risks Flagged)</h3>
                
                {failureResults.length === 0 ? (
                  <div className="glass-card" style={{ border: '1px solid rgba(16,185,129,0.2)', background: 'rgba(16,185,129,0.02)', textAlign: 'center' }}>
                    <h4 style={{ color: '#10b981' }}>✅ Strategy Cleared</h4>
                    <p style={{ fontSize: '13px', marginTop: '6px', color: '#94a3b8' }}>No immediate alignment with failure database parameters detected.</p>
                  </div>
                ) : (
                  failureResults.map((p, idx) => (
                    <div key={idx} className="glass-card" style={{ borderLeft: '4px solid var(--accent-red)', background: 'rgba(244,63,94,0.02)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                        <h4 style={{ color: 'var(--accent-red)' }}>❌ {p.name}</h4>
                        <span className="badge" style={{ background: '#f43f5e', color: 'white' }}>Risk rate: {p.failure_rate}</span>
                      </div>
                      <p style={{ fontSize: '13px', lineHeight: '1.5', color: '#cbd5e1', marginBottom: '8px' }}>
                        <strong>The Lesson:</strong> {p.lesson}
                      </p>
                      <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                        <strong>Examples:</strong>
                        <ul style={{ paddingLeft: '20px', marginTop: '4px' }}>
                          {p.examples.map((ex, exIdx) => <li key={exIdx}>{ex}</li>)}
                        </ul>
                      </div>
                      <div style={{ background: 'rgba(16,185,129,0.06)', border: '1px solid rgba(16,185,129,0.1)', padding: '12px', borderRadius: '8px', color: '#a7f3d0', fontSize: '13px' }}>
                        <strong>💡 Correction:</strong> {p.fix}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        )}

        {/* 🤖 Autopilot Suite Tab */}
        {activeTab === "autopilot" && (
          <div>
            <h1 className="page-title">🤖 Startup Autopilot Suite</h1>
            <p className="page-subtitle">Ghost Founder monitors competitors and drafts strategy briefs while you sleep.</p>

            <div className="tab-nav">
              <div className={`tab-nav-item ${autopilotTab === 'brief' ? 'active' : ''}`} onClick={() => setAutopilotTab('brief')}>
                📋 Monday Brief
              </div>
              <div className={`tab-nav-item ${autopilotTab === 'competitor' ? 'active' : ''}`} onClick={() => setAutopilotTab('competitor')}>
                🛡️ Competitor Watch
              </div>
              <div className={`tab-nav-item ${autopilotTab === 'email' ? 'active' : ''}`} onClick={() => setAutopilotTab('email')}>
                ✉️ Customer Email Helper
              </div>
            </div>

            {/* Sub-Tab 1: Monday Brief */}
            {autopilotTab === "brief" && (
              <div className="glass-card">
                <h3>Weekly Action Assessment</h3>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Ghost Founder scans decision records to compile core metrics and warnings.</p>
                
                <button 
                  className="btn-primary" 
                  style={{ width: '100%', marginBottom: '20px' }}
                  onClick={generateAutopilotBrief}
                  disabled={isBriefLoading}
                >
                  {isBriefLoading ? "Analyzing history logs..." : "📋 Generate Monday Briefing"}
                </button>

                {weeklyBrief && (
                  <div style={{ background: '#111119', border: '1px solid #1e1e2d', padding: '24px', borderRadius: '12px' }}>
                    <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginBottom: '16px' }}>
                      Generated at {weeklyBrief.generated_at} (based on {weeklyBrief.based_on} inputs)
                    </div>
                    <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', fontSize: '14px', color: '#e2e8f0' }} className="markdown-render">
                      {weeklyBrief.brief}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Sub-Tab 2: Competitor Watch */}
            {autopilotTab === "competitor" && (
              <div className="glass-card">
                <h3>Surveillance Tracker</h3>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '20px' }}>Simulate competitor tracking analysis.</p>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                  <div className="input-group">
                    <span className="input-label">Your Company Profile</span>
                    <input 
                      type="text" 
                      className="input-field" 
                      value={startupDesc}
                      onChange={e => setStartupDesc(e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="input-label">Competitor Name</span>
                    <input 
                      type="text" 
                      className="input-field" 
                      placeholder="e.g. Linear"
                      value={competitorName}
                      onChange={e => setCompetitorName(e.target.value)}
                    />
                  </div>
                </div>

                <button 
                  className="btn-primary" 
                  style={{ width: '100%', marginBottom: '20px' }}
                  onClick={getCompetitorIntelligence}
                  disabled={isCompetitorLoading}
                >
                  {isCompetitorLoading ? "Monitoring competitor streams..." : "🛡️ Scan Competitor"}
                </button>

                {competitorReport && (
                  <div style={{ background: '#111119', border: '1px solid #1e1e2d', padding: '24px', borderRadius: '12px', whiteSpace: 'pre-wrap', fontSize: '14px', lineHeight: '1.6' }}>
                    {competitorReport}
                  </div>
                )}
              </div>
            )}

            {/* Sub-Tab 3: Email Drafts */}
            {autopilotTab === "email" && (
              <div className="glass-card">
                <h3>Strategic Support Responder</h3>
                <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>Reply to emails without violating core rules (e.g. pricing/feature parameters in memory).</p>

                <div className="input-group" style={{ marginBottom: '16px' }}>
                  <span className="input-label">Select Customer Inquiry Email</span>
                  <select 
                    className="input-field" 
                    value={customerEmail}
                    onChange={e => setCustomerEmail(e.target.value)}
                  >
                    <option value="Your product is too expensive for small teams. Can we get a 50% discount?">Can we get a 50% discount? (Checks pricing discount block)</option>
                    <option value="I want you to build a calendar integration and a kanban view before our team signs up. Can you do this next week?">Can you build 3 features next week? (Checks feature freeze block)</option>
                    <option value="Can we get a custom enterprise contract with custom SLAs? We are 4 users.">Can we get custom enterprise SLAs for 4 users?</option>
                  </select>
                </div>

                <button 
                  className="btn-primary" 
                  style={{ width: '100%', marginBottom: '20px' }}
                  onClick={runDraftResponse}
                  disabled={isEmailLoading}
                >
                  {isEmailLoading ? "Drafting email..." : "✍️ Generate Strategic Reply"}
                </button>

                {emailDraft && (
                  <div style={{ background: '#0e0e15', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '20px' }}>
                    <h5 style={{ color: '#a78bfa', fontSize: '12px', textTransform: 'uppercase', marginBottom: '8px' }}>Strategic Draft Reply:</h5>
                    <div style={{ whiteSpace: 'pre-wrap', fontSize: '13px', lineHeight: '1.5', padding: '12px', background: '#06060c', border: '1px solid #181824', borderRadius: '8px', color: '#cbd5e1' }}>
                      {emailDraft}
                    </div>
                    {emailMeta && (
                      <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '10px' }}>
                        Routed via {emailMeta.model} in {emailMeta.latency}ms
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* ⚡ Routing Dashboard Tab */}
        {activeTab === "routing" && (
          <div>
            <h1 className="page-title">⚡ cascadeflow Routing logs</h1>
            <p className="page-subtitle">Visual demonstration proving how cascadeflow routes simple requests to fast nodes and saves budget live.</p>

            <div className="dashboard-metrics">
              <div className="metric-box">
                <div className="metric-title">TOTAL QUERIES</div>
                <div className="metric-value blue">{routingStats.total}</div>
                <div className="metric-sub">{routingStats.fast} fast | {routingStats.power} power</div>
              </div>
              <div className="metric-box">
                <div className="metric-title">AVG INFERENCE SPEED</div>
                <div className="metric-value green">{routingStats.avgLatency} ms</div>
                <div className="metric-sub">Auto model mapping</div>
              </div>
              <div className="metric-box">
                <div className="metric-title">TOTAL ROUTED COST</div>
                <div className="metric-value">${routingStats.totalCost.toFixed(5)}</div>
                <div className="metric-sub">Static Llama-70B: ${routingStats.staticCost.toFixed(5)}</div>
              </div>
              <div className="metric-box" style={{ borderColor: 'rgba(16,185,129,0.2)' }}>
                <div className="metric-title" style={{ color: 'var(--accent-green)' }}>FUNDS BUDGET SAVED</div>
                <div className="metric-value" style={{ color: 'var(--accent-green)' }}>{routingStats.savedPct}%</div>
                <div className="metric-sub">Saved: ${routingStats.saved.toFixed(5)}</div>
              </div>
            </div>

            <div className="dashboard-charts">
              {/* Chart 1: Donut/Gauge */}
              <div className="glass-card" style={{ height: '340px' }}>
                <h4 style={{ fontSize: '14px', marginBottom: '16px' }}>Model Selection Distribution</h4>
                <div className="chart-container-svg">
                  <svg width="200" height="200" viewBox="0 0 200 200">
                    <circle cx="100" cy="100" r="80" fill="none" stroke="#1f1f2e" strokeWidth="20" />
                    
                    {routingStats.total > 0 && (
                      <circle 
                        cx="100" 
                        cy="100" 
                        r="80" 
                        fill="none" 
                        stroke="#10b981" 
                        strokeWidth="20" 
                        strokeDasharray={`${(routingStats.fast / routingStats.total) * 502} 502`}
                        transform="rotate(-90 100 100)"
                      />
                    )}
                    <text x="100" y="95" fill="white" fontSize="24" fontWeight="800" textAnchor="middle">
                      {routingStats.total}
                    </text>
                    <text x="100" y="120" fill="var(--text-muted)" fontSize="10" fontWeight="600" textAnchor="middle">
                      TOTAL QUERIES
                    </text>
                  </svg>
                </div>
                <div style={{ display: 'flex', justifyContent: 'center', gap: '24px', fontSize: '11px', marginTop: '-10px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <div style={{ width: '12px', height: '12px', background: '#10b981', borderRadius: '3px' }}></div>
                    <span>Fast (llama3-8b): {routingStats.fast}</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <div style={{ width: '12px', height: '12px', background: '#1f1f2e', borderRadius: '3px' }}></div>
                    <span>Power (llama-70b): {routingStats.power}</span>
                  </div>
                </div>
              </div>

              {/* Chart 2: Latency Timeline */}
              <div className="glass-card" style={{ height: '340px' }}>
                <h4 style={{ fontSize: '14px', marginBottom: '16px' }}>Speed & Latency Trends (ms)</h4>
                <div className="chart-container-svg" style={{ padding: '0 10px' }}>
                  {routingLog.length < 2 ? (
                    <div style={{ color: 'var(--text-muted)', fontSize: '12px' }}>Waiting for more logs to render timeline...</div>
                  ) : (
                    <svg width="100%" height="180">
                      {/* Grid lines */}
                      <line x1="30" y1="20" x2="95%" y2="20" stroke="#1c1c28" strokeWidth="1" />
                      <line x1="30" y1="80" x2="95%" y2="80" stroke="#1c1c28" strokeWidth="1" />
                      <line x1="30" y1="140" x2="95%" y2="140" stroke="#1c1c28" strokeWidth="1" />
                      
                      {/* Map lines */}
                      {(() => {
                        const maxVal = Math.max(...routingLog.map(r => r.latency_ms), 1000);
                        const points = routingLog.map((r, i) => {
                          const x = 40 + (i / (routingLog.length - 1)) * 260;
                          const y = 150 - (r.latency_ms / maxVal) * 120;
                          return `${x},${y}`;
                        }).join(' ');

                        return (
                          <>
                            <polyline fill="none" stroke="#7c3aed" strokeWidth="3" points={points} />
                            {routingLog.map((r, i) => {
                              const x = 40 + (i / (routingLog.length - 1)) * 260;
                              const y = 150 - (r.latency_ms / maxVal) * 120;
                              return (
                                <g key={i}>
                                  <circle cx={x} cy={y} r="5" fill="#10b981" stroke="white" strokeWidth="1.5" />
                                  <text x={x} y={y - 10} fill="#94a3b8" fontSize="8" textAnchor="middle">{r.latency_ms}ms</text>
                                </g>
                              );
                            })}
                          </>
                        );
                      })()}
                    </svg>
                  )}
                </div>
              </div>
            </div>

            {/* Execution Table Log */}
            <h3 style={{ marginTop: '30px' }}>Recent Request Routing Stream</h3>
            <div className="glass-card log-table-container">
              <table className="log-table">
                <thead>
                  <tr>
                    <th>Prompt</th>
                    <th>Routed Model</th>
                    <th>Latency</th>
                    <th>Cost</th>
                    <th>Savings</th>
                    <th>Execution Type</th>
                  </tr>
                </thead>
                <tbody>
                  {routingLog.slice().reverse().map((r, idx) => (
                    <tr key={idx}>
                      <td style={{ fontFamily: 'monospace', color: '#a78bfa' }}>{r.question}</td>
                      <td>{r.model}</td>
                      <td>{r.latency_ms} ms</td>
                      <td>${(r.cost || 0).toFixed(6)}</td>
                      <td style={{ color: '#10b981', fontWeight: 600 }}>${(r.cost_saved || 0).toFixed(6)}</td>
                      <td>{r.is_mock ? "🟡 Simulated" : "🟢 Live API"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* 🧠 Founder Pulse Tab */}
        {activeTab === "mood" && (
          <div>
            <h1 className="page-title">🧠 Founder Pulse</h1>
            <p className="page-subtitle">Emotional intelligence layer. Ghost Founder tracks your mood, detects burnout, and warns you before panic-driven decisions.</p>

            {/* Mood Hero Section */}
            <div className="mood-hero">
              <div className="mood-indicator-card" style={{ borderColor: currentMood?.currentMood?.color || 'var(--border-color)' }}>
                <div className="mood-emoji">
                  {currentMood?.currentMoodKey === 'calm' ? '😌' :
                   currentMood?.currentMoodKey === 'excited' ? '🚀' :
                   currentMood?.currentMoodKey === 'anxious' ? '😰' :
                   currentMood?.currentMoodKey === 'panic' ? '🔥' :
                   currentMood?.currentMoodKey === 'overconfident' ? '⚡' :
                   currentMood?.currentMoodKey === 'fatigued' ? '😴' :
                   currentMood?.currentMoodKey === 'desperate' ? '🆘' : '😌'}
                </div>
                <div className="mood-label" style={{ color: currentMood?.currentMood?.color || '#10b981' }}>
                  {currentMood?.currentMood?.label || '😌 Calm & Focused'}
                </div>
                <div className="mood-advice">
                  {currentMood?.currentMood?.advice || 'Start chatting to begin mood tracking.'}
                </div>
              </div>

              <div className="stability-meter">
                <div className="stability-value" style={{ color: (moodTimeline?.averageStability || 70) > 60 ? '#10b981' : (moodTimeline?.averageStability || 70) > 40 ? '#f59e0b' : '#ef4444' }}>
                  {moodTimeline?.averageStability || 70}
                </div>
                <div className="stability-label">Average Stability Score</div>
                <div className="stability-bar-container">
                  <div
                    className="stability-bar-fill"
                    style={{
                      width: `${moodTimeline?.averageStability || 70}%`,
                      background: (moodTimeline?.averageStability || 70) > 60 ? '#10b981' : (moodTimeline?.averageStability || 70) > 40 ? '#f59e0b' : '#ef4444'
                    }}
                  />
                </div>
              </div>
            </div>

            {/* Stats Row */}
            <div className="mood-stats-row">
              <div className="mood-stat-card">
                <div className="mood-stat-value">{moodTimeline?.totalEntries || 0}</div>
                <div className="mood-stat-label">Messages Analyzed</div>
              </div>
              <div className="mood-stat-card">
                <div className="mood-stat-value" style={{ color: '#f59e0b' }}>{moodTimeline?.warningCount || 0}</div>
                <div className="mood-stat-label">Warning Events</div>
              </div>
              <div className="mood-stat-card">
                <div className="mood-stat-value" style={{ color: '#10b981' }}>
                  {moodTimeline?.entries?.length > 0
                    ? Math.round(moodTimeline.entries.filter(e => e.mood === 'calm' || e.mood === 'excited').length / moodTimeline.entries.length * 100)
                    : 100}%
                </div>
                <div className="mood-stat-label">Positive Mood Rate</div>
              </div>
            </div>

            {/* Mood Timeline Log */}
            <div className="mood-timeline-card">
              <h4 style={{ fontSize: '14px', marginBottom: '16px' }}>📈 Mood Timeline</h4>
              {(!moodTimeline?.entries || moodTimeline.entries.length === 0) ? (
                <div style={{ color: 'var(--text-muted)', fontSize: '13px', textAlign: 'center', padding: '20px' }}>
                  No mood data yet. Start chatting in Strategy Chat to build your emotional timeline.
                </div>
              ) : (
                moodTimeline.entries.slice().reverse().map((entry, idx) => (
                  <div className="mood-timeline-entry" key={idx}>
                    <div className="mood-timeline-dot" style={{ background: entry.mood === 'calm' ? '#10b981' : entry.mood === 'excited' ? '#6366f1' : entry.mood === 'panic' ? '#ef4444' : entry.mood === 'fatigued' ? '#ec4899' : entry.mood === 'desperate' ? '#dc2626' : entry.mood === 'overconfident' ? '#f97316' : '#f59e0b' }} />
                    <div className="mood-timeline-text">
                      <strong>{entry.label}</strong> — {entry.messagePreview}
                    </div>
                    <div className="mood-timeline-score" style={{ color: entry.stabilityScore > 60 ? '#10b981' : entry.stabilityScore > 40 ? '#f59e0b' : '#ef4444' }}>
                      {entry.stabilityScore}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}

        {/* 💀 Startup Graveyard Tab */}
        {activeTab === "graveyard" && (
          <div>
            <h1 className="page-title">💀 Startup Graveyard</h1>
            <p className="page-subtitle">Describe your strategy and we'll show you which dead startups walked the same path — and where they fell.</p>

            {/* Strategy Input */}
            <div className="glass-card graveyard-input-section">
              <h3 style={{ marginBottom: '16px' }}>Describe Your Current Strategy</h3>
              <textarea
                className="input-field"
                style={{ width: '100%', minHeight: '100px', resize: 'none', marginBottom: '16px' }}
                placeholder="e.g. We want to raise $2M in funding, scale to 5 new cities, offer aggressive discounts to undercut competitors, and hire 10 engineers before we have product-market fit..."
                value={graveyardStrategy}
                onChange={e => setGraveyardStrategy(e.target.value)}
              />
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', marginBottom: '16px' }}>
                <button className="btn-secondary" onClick={() => setGraveyardStrategy("We want to raise $5M in venture capital, scale to 10 cities immediately, and hire 15 engineers. We'll offer heavy discounts to undercut our biggest competitor and build every feature customers ask for.")}>⚡ Aggressive Scale</button>
                <button className="btn-secondary" onClick={() => setGraveyardStrategy("We're going to build in stealth mode for 6 months without talking to any customers. We'll launch with a premium price and spend heavily on marketing with a Super Bowl ad to create brand awareness.")}>🕵️ Stealth Launch</button>
                <button className="btn-secondary" onClick={() => setGraveyardStrategy("We're pivoting our product for the third time. We started as a social network, then tried flash sales, and now we want to do e-commerce. We need to hire fast and expand quickly.")}>🔄 Serial Pivot</button>
              </div>
              <button
                className="btn-primary"
                style={{ width: '100%' }}
                onClick={compareToGraveyard}
                disabled={isGraveyardLoading || !graveyardStrategy.trim()}
              >
                {isGraveyardLoading ? '💀 Searching the graveyard...' : '💀 Compare Against Dead Startups'}
              </button>
            </div>

            {/* Results */}
            {graveyardResults && (
              <div>
                {graveyardResults.matchCount === 0 ? (
                  <div className="glass-card graveyard-empty">
                    <div style={{ fontSize: '48px', marginBottom: '16px' }}>✅</div>
                    <strong>No matches found in the graveyard!</strong><br/>
                    Your strategy doesn't closely mirror any of the failed startups in our database. Stay vigilant.
                  </div>
                ) : (
                  <div>
                    <div style={{ marginBottom: '16px', color: '#fca5a5', fontSize: '14px', fontWeight: 600 }}>
                      ⚠️ Found {graveyardResults.matchCount} dead startup{graveyardResults.matchCount > 1 ? 's' : ''} with a similar path:
                    </div>
                    <div className="graveyard-results">
                      {graveyardResults.matches.map((match, idx) => (
                        <div className="graveyard-card" key={idx}>
                          <div className="graveyard-card-header">
                            <div className="graveyard-card-title">
                              <span className="graveyard-icon">{match.icon}</span>
                              <div>
                                <div className="graveyard-name">{match.name}</div>
                                <div className="graveyard-meta">Raised: {match.raised} · Lived: {match.lifespan}</div>
                              </div>
                            </div>
                            <span
                              className="graveyard-danger-badge"
                              style={{
                                background: match.dangerScore > 60 ? 'rgba(239,68,68,0.15)' : match.dangerScore > 30 ? 'rgba(245,158,11,0.15)' : 'rgba(255,255,255,0.05)',
                                color: match.dangerScore > 60 ? '#ef4444' : match.dangerScore > 30 ? '#f59e0b' : 'var(--text-muted)'
                              }}
                            >
                              {match.dangerScore}% Danger
                            </span>
                          </div>

                          <div className="graveyard-death-cause">💀 {match.deathCause}</div>

                          <div className="graveyard-danger-bar">
                            <div
                              className="graveyard-danger-fill"
                              style={{
                                width: `${match.dangerScore}%`,
                                background: match.dangerScore > 60 ? 'linear-gradient(90deg, #ef4444, #dc2626)' : match.dangerScore > 30 ? 'linear-gradient(90deg, #f59e0b, #d97706)' : 'linear-gradient(90deg, #6366f1, #4f46e5)'
                              }}
                            />
                          </div>

                          <div className="graveyard-stages">
                            {Array.from({ length: match.totalStages }, (_, i) => {
                              const matchedStage = match.matchedStages.find(s => s.stageIndex === i);
                              return (
                                <span key={i} className={`graveyard-stage-pill ${matchedStage ? 'matched' : 'unmatched'}`}>
                                  {matchedStage ? '🔴' : '⚪'} Stage {i + 1}
                                </span>
                              );
                            })}
                          </div>

                          <div className="graveyard-lesson">
                            <div className="graveyard-lesson-title">📖 Lesson Learned</div>
                            <div className="graveyard-lesson-text">{match.lesson}</div>
                          </div>

                          <div className="graveyard-survival">
                            <div className="graveyard-survival-title">🛡️ What They Should Have Done</div>
                            <div className="graveyard-survival-text">{match.survivalAdvice}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}

export default App;
