param(
  [ValidateSet("hermes","openclaw","codex","claude","agents","all")]
  [string]$Target = "all",
  [string]$SourceDir = (Split-Path -Parent $MyInvocation.MyCommand.Path)
)
$ErrorActionPreference="Stop"
$Source=(Resolve-Path -LiteralPath $SourceDir).Path
$Name="ru-seo-agent"
if(-not (Test-Path -LiteralPath (Join-Path $Source "SKILL.md"))){throw "SourceDir must contain SKILL.md: $Source"}
$targets=@{
  hermes=(Join-Path $HOME ".hermes\skills")
  openclaw=(Join-Path $HOME ".openclaw\skills")
  codex=(Join-Path $HOME ".codex\skills")
  claude=(Join-Path $HOME ".claude\skills")
  agents=(Join-Path $HOME ".agents\skills")
}
function Install-Skill([string]$Base){
  New-Item -ItemType Directory -Force -Path $Base | Out-Null
  $Dest=Join-Path $Base $Name
  if(Test-Path $Dest){
    $resolvedBase=(Resolve-Path -LiteralPath $Base).Path
    $resolvedDest=(Resolve-Path -LiteralPath $Dest).Path
    if($resolvedDest -ne (Join-Path $resolvedBase $Name)){throw "Unsafe destination: $resolvedDest"}
    Remove-Item -LiteralPath $resolvedDest -Recurse -Force
  }
  Copy-Item -Recurse -Force $Source $Dest
  Write-Host "Installed: $Dest"
}
if($Target -eq "all"){
  foreach($k in @("hermes","openclaw","agents","codex","claude")){Install-Skill $targets[$k]}
}else{Install-Skill $targets[$Target]}
