
import { useState } from "react";
import "./App.css";

const languages = [
  { code: "en", name: "English" },
  { code: "hi", name: "Hindi" },
  { code: "te", name: "Telugu" },
  { code: "gu", name: "Gujarati" },
];

function App() {
  const [mode, setMode] = useState("translation");
  const [sourceLanguage, setSourceLanguage] = useState("en");
  const [targetLanguage, setTargetLanguage] = useState("hi");
  const [text, setText] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleConvert() {
    if (!text.trim()) {
      setError("Please enter some text first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");

    try {
      const response = await fetch("http://127.0.0.1:8000/convert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text,
          mode,
          source_language:
            mode === "transliteration" ? "en" : sourceLanguage,
          target_language: targetLanguage,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Conversion failed.");
      }

      setResult(data.output);
    } catch (err) {
      setError(err.message || "Could not connect to BHASHA AI.");
    } finally {
      setLoading(false);
    }
  }

  async function copyResult() {
    if (!result) return;

    try {
      await navigator.clipboard.writeText(result);
    } catch {
      setError("Could not copy the output. Please select and copy it manually.");
    }
  }

  function clearInput() {
    setText("");
    setError("");
  }

  function clearOutput() {
    setResult("");
    setError("");
  }

  function changeMode(newMode) {
    setMode(newMode);
    setResult("");
    setError("");
  }

  return (
    <div className="app">
      <header className="navbar">
        <div className="logo">
          <span className="logo-symbol">भ</span>
          <span>BHASHA AI</span>
        </div>

        <span className="tagline">
          INDIAN MULTILINGUAL NLP
        </span>
      </header>

      <main>
        <section className="heading">
          <h1>Break Language Barriers</h1>
          <p>
            Understand languages. Connect without boundaries.
          </p>
        </section>

        <section className="translator">
          <div className="mode-selector">
            <button
              className={mode === "translation" ? "selected" : ""}
              onClick={() => changeMode("translation")}
            >
              Translation
            </button>

            <button
              className={mode === "transliteration" ? "selected" : ""}
              onClick={() => changeMode("transliteration")}
            >
              Transliteration
            </button>
          </div>

          <div className="language-bar">
            <div>
              <label>FROM</label>

              {mode === "transliteration" ? (
                <div className="fixed-language">
                  Roman Script
                </div>
              ) : (
                <select
                  value={sourceLanguage}
                  onChange={(e) => {
                    setSourceLanguage(e.target.value);
                    setResult("");
                  }}
                >
                  {languages.map((language) => (
                    <option key={language.code} value={language.code}>
                      {language.name}
                    </option>
                  ))}
                </select>
              )}
            </div>

            <span className="swap">⇄</span>

            <div>
              <label>TO</label>

              <select
                value={targetLanguage}
                onChange={(e) => {
                  setTargetLanguage(e.target.value);
                  setResult("");
                }}
              >
                {languages
                  .filter((language) =>
                    mode === "transliteration"
                      ? language.code !== "en"
                      : language.code !== sourceLanguage
                  )
                  .map((language) => (
                    <option key={language.code} value={language.code}>
                      {language.name}
                    </option>
                  ))}
              </select>
            </div>
          </div>

          <div className="panels">
            <div className="panel">
              <div className="panel-title">
                <strong>Source Text</strong>
                <button onClick={clearInput}>Clear</button>
              </div>

              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder={
                  mode === "translation"
                    ? "Enter text to translate..."
                    : "Type Romanized text here..."
                }
              />

              <small>{text.length} characters</small>
            </div>

            <div className="panel output-panel">
              <div className="panel-title">
                <strong>
                  {mode === "translation"
                    ? "Translation"
                    : "Transliteration"}
                </strong>

                <div className="output-actions">
                  <button onClick={copyResult} disabled={!result}>
                    Copy
                  </button>
                  <button onClick={clearOutput}>Clear</button>
                </div>
              </div>

              <div className={`result ${!result ? "placeholder" : ""}`}>
                {result || "Your output will appear here..."}
              </div>
            </div>
          </div>

          {error && <div className="error-message">{error}</div>}

          <button
            className="convert-button"
            onClick={handleConvert}
            disabled={loading}
          >
            {loading
              ? "Processing..."
              : mode === "translation"
                ? "Translate"
                : "Transliterate"}
          </button>

          <p className="note">
            Powered by BHASHA AI · Indian Multilingual NLP
          </p>
        </section>
      </main>

      <footer>
        BHASHA AI · Built for Indian Languages
      </footer>
    </div>
  );
}

export default App;
