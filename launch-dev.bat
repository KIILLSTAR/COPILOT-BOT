# bootstrap.ps1

Write-Host "🚀 Bootstrapping ETH Perps Dev Environment..."

# 1. Create virtual environment if missing
if (!(Test-Path ".\venv")) {
    Write-Host "🔧 Creating Python virtual environment..."
    python -m venv venv
}

# 2. Activate virtual environment
Write-Host "✅ Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

# 3. Install dependencies
Write-Host "📦 Installing Python packages..."
pip install -r requirements.txt

# 4. Start Ollama if not running
Write-Host "🧠 Checking Ollama status..."
$ollamaStatus = & tasklist | Select-String "ollama"
if (-not $ollamaStatus) {
    Write-Host "🧠 Starting Ollama with CodeLlama 34B..."
    Start-Process "ollama" -ArgumentList "run codellama:34b"
} else {
    Write-Host "🧠 Ollama already running."
}

# 5. Link Continue.dev config
$continueConfig = "$env:USERPROFILE\.continue\config.json"
$repoConfig = ".\.continue\config.json"
if (Test-Path $repoConfig) {
    Write-Host "🔗 Linking Continue.dev config..."
    Copy-Item $repoConfig $continueConfig -Force
}

# 6. Launch VS Code
Write-Host "🖥️ Launching VS Code..."
Start-Process "code" -ArgumentList "."

Write-Host "✅ All systems go. Happy coding, Nate!"
