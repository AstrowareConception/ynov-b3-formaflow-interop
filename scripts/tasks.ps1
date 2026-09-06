param([Parameter(Position=0)][string]$Task = "help")
$ErrorActionPreference = "Stop"
$python = if (Get-Command py -ErrorAction SilentlyContinue) { @("py", "-3.12") } else { @("python") }
if ($python.Count -eq 2) { & $python[0] $python[1] "scripts/tasks.py" $Task } else { & $python[0] "scripts/tasks.py" $Task }
exit $LASTEXITCODE

