# Splices the hand-authored parts of one map into the single SketchLayout document the API takes.
# It substitutes a named HouseStyle into each house prop that names one and concatenates the pieces -
# it computes no coordinate, no placement and no validation. Everything geometric is authored by hand
# in shapes.json / props.json / styles.json.
param(
  [Parameter(Mandatory = $true)][string]$Dir,
  [string]$Out = 'layout.json'
)

$ErrorActionPreference = 'Stop'

# Read inline rather than through a helper: ConvertFrom-Json hands an array to the pipeline as one
# object, and a function's return re-wraps it, so @(Read-Doc 'props.json') yields a single element.
$base   = Get-Content (Join-Path $Dir 'base.json')   -Raw | ConvertFrom-Json   # setup, mapTheme, themes, roomStyles, relief
$shapes = Get-Content (Join-Path $Dir 'shapes.json') -Raw | ConvertFrom-Json   # layout.islands + layout.shapes
$styles = Get-Content (Join-Path $Dir 'styles.json') -Raw | ConvertFrom-Json   # named HouseStyle snapshots
$props  = Get-Content (Join-Path $Dir 'props.json')  -Raw | ConvertFrom-Json   # the authored prop list

foreach ($p in $props) {
  if ($p.kind -ne 'house') { continue }
  $name = [string]$p.style
  if (-not $styles.PSObject.Properties[$name]) { throw "house '$($p.id)' names unknown style '$name'" }
  # Add-Member -Force, not assignment: the property arrived from JSON typed as a string, and a plain
  # assignment would coerce the style object back into one.
  $p | Add-Member -NotePropertyName style -NotePropertyValue $styles.$name -Force
}

# Each array is serialized on its own and spliced in as text. PowerShell 5.1's ConvertTo-Json re-wraps
# an Object[] that came from ConvertFrom-Json in a {"value": [...], "Count": n} envelope when it is
# nested inside another object, which is not the wire shape; piping the array into ConvertTo-Json so it
# is the top-level value avoids that entirely.
# ...and a one-element array unrolls to a bare object on the way in, so the brackets go back on by hand.
function ConvertTo-JsonArray($items) {
  $list = @($items)
  if ($list.Count -eq 0) { return '[]' }
  $text = $list | ConvertTo-Json -Depth 60
  if ($text.TrimStart().StartsWith('[')) { return $text }
  return "[$text]"
}

$islandsJson = ConvertTo-JsonArray $shapes.islands
$shapesJson  = ConvertTo-JsonArray $shapes.shapes
$propsJson   = ConvertTo-JsonArray $props

$doc = [ordered]@{
  setup      = $base.setup
  layout     = '@@LAYOUT@@'
  mapTheme   = $base.mapTheme
  themes     = $base.themes
  roomStyles = $base.roomStyles
  relief     = $base.relief
  dressing   = '@@DRESSING@@'
}

$layoutJson   = "{ ""islands"": $islandsJson, ""shapes"": $shapesJson }"
$dressingJson = "{ ""props"": $propsJson }"

$text = $doc | ConvertTo-Json -Depth 60
$text = $text.Replace('"@@LAYOUT@@"', $layoutJson).Replace('"@@DRESSING@@"', $dressingJson)

# Fail loudly rather than writing a document the API will read as half a map.
$check = $text | ConvertFrom-Json
if (@($check.layout.shapes).Count -ne @($shapes.shapes).Count) { throw 'shape count did not survive assembly' }
if (@($check.dressing.props).Count -ne @($props).Count)        { throw 'prop count did not survive assembly' }

$text | Set-Content (Join-Path $Dir $Out) -Encoding utf8
"assembled $Out - $(@($check.layout.shapes).Count) shapes, $(@($check.dressing.props).Count) props, $(@($styles.PSObject.Properties).Count) house styles"
