# drive.ps1 — a thin poster for the pgm-studio authoring endpoints.
# It composes nothing and validates nothing: every call below is documented in docs/tools/plan.md
# "Driving it without the UI". All geometry, themes, styles and dressing are authored by hand in JSON.

$script:Api = 'http://localhost:5189/api'

function Send-Json {
    param([string]$Method, [string]$Path, [string]$Json)
    $uri = "$script:Api/$Path"
    $args = @{ Uri = $uri; Method = $Method; ContentType = 'application/json; charset=utf-8'; TimeoutSec = 300 }
    if ($PSBoundParameters.ContainsKey('Json') -and $Json) {
        $args.Body = [System.Text.Encoding]::UTF8.GetBytes($Json)
    }
    try {
        return Invoke-RestMethod @args
    } catch {
        $resp = $_.Exception.Response
        $body = ''
        if ($resp) {
            try {
                $reader = New-Object System.IO.StreamReader($resp.GetResponseStream())
                $body = $reader.ReadToEnd()
            } catch { }
        }
        $code = ''
        if ($resp) { $code = [int]$resp.StatusCode }
        throw "HTTP $code $Method $uri`n$body"
    }
}

function Send-File {
    param([string]$Method, [string]$Path, [string]$File)
    return Send-Json -Method $Method -Path $Path -Json (Get-Content $File -Raw)
}

function New-PlanMap {
    param([string]$Name)
    $r = Send-Json -Method POST -Path 'plan' -Json (@{ name = $Name } | ConvertTo-Json -Compress)
    return $r.slug
}

function Test-PlanDoc  { param([string]$File) Send-File -Method POST -Path 'plan/evaluate' -File $File }
function Get-PlanCompile { param([string]$File) Send-File -Method POST -Path 'plan/compile'  -File $File }
function Set-MapPlan   { param([string]$Slug,[string]$File) Send-File -Method PUT -Path "map/$Slug/plan" -File $File }
function Set-MapSketch { param([string]$Slug,[string]$File) Send-File -Method PUT -Path "map/$Slug/sketch" -File $File }
function Complete-MapSketch { param([string]$Slug) Send-Json -Method POST -Path "map/$Slug/sketch/finish" }
function Set-MapIntent { param([string]$Slug,[string]$File) Send-File -Method PUT -Path "map/$Slug/intent/from-plan" -File $File }
function Get-MapLayers { param([string]$Slug) Send-Json -Method GET -Path "map/$Slug/layers" }

function Export-Map {
    param([string]$Slug, [string]$OutDir)
    # B102: a rebuild writes over a region dir it never clears — always export into a fresh empty directory.
    if (Test-Path $OutDir) { Remove-Item $OutDir -Recurse -Force }
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
    $zip = Join-Path $OutDir 'export.zip'
    Invoke-WebRequest -Uri "$script:Api/map/$Slug/export" -OutFile $zip -TimeoutSec 600
    Expand-Archive -Path $zip -DestinationPath $OutDir -Force
    Remove-Item $zip
    return (Get-ChildItem $OutDir -Recurse | Measure-Object).Count
}

function Save-Json {
    param($Object, [string]$File)
    $Object | ConvertTo-Json -Depth 40 | Set-Content $File -Encoding utf8
}
