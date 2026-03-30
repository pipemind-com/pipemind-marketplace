# Bootstrap script for mcp-semantic-scholar (Windows)
# Downloads the pre-built binary from GitHub Releases on first run.
$ErrorActionPreference = "Stop"

$Repo = "pipemind-com/agentic-marketplace"
$BinDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$CacheDir = Join-Path $BinDir ".cache"
$Artifact = "mcp-semantic-scholar-windows-x64.exe"
$Binary = Join-Path $CacheDir $Artifact

# Resolve expected version from plugin.json
$PluginJson = Join-Path $BinDir ".." ".claude-plugin" "plugin.json"
$ExpectedVersion = ""
if (Test-Path $PluginJson) {
    $plugin = Get-Content $PluginJson | ConvertFrom-Json
    $ExpectedVersion = $plugin.version
}

$VersionFile = Join-Path $CacheDir ".version"

# Check if cached binary matches expected version
$NeedDownload = $false
if (-not (Test-Path $Binary)) {
    $NeedDownload = $true
} elseif ($ExpectedVersion -and (Test-Path $VersionFile)) {
    $CachedVersion = (Get-Content $VersionFile -Raw).Trim()
    if ($CachedVersion -ne $ExpectedVersion) {
        $NeedDownload = $true
    }
} elseif ($ExpectedVersion -and -not (Test-Path $VersionFile)) {
    $NeedDownload = $true
}

if ($NeedDownload) {
    New-Item -ItemType Directory -Force -Path $CacheDir | Out-Null
    # Tags use plugin/vX.Y.Z format; URL-encode the slash as %2F
    $Tag = "mcp-semantic-scholar%2Fv$ExpectedVersion"
    $Url = "https://github.com/$Repo/releases/download/$Tag/$Artifact"
    # Download to a temp file first, then move over the target.
    # Writing directly to $Binary fails if the old binary is still running
    # (Windows file locking / Linux ETXTBSY).
    $TmpBinary = "$Binary.tmp.$PID"

    [Console]::Error.WriteLine("Downloading mcp-semantic-scholar $ExpectedVersion for Windows...")
    try {
        Invoke-WebRequest -Uri $Url -OutFile $TmpBinary -UseBasicParsing
        Move-Item -Force $TmpBinary $Binary
        Set-Content -Path $VersionFile -Value $ExpectedVersion
        [Console]::Error.WriteLine("Downloaded mcp-semantic-scholar $ExpectedVersion")
    } catch {
        Remove-Item -ErrorAction SilentlyContinue $TmpBinary
        throw
    }
}

& $Binary @args
