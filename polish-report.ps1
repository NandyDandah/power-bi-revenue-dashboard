$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot 'Power BI Project.Report/definition/pages'
function Lit($value) { @{expr=@{Literal=@{Value=$value}}} }
function Color($value) { @{solid=@{color=(Lit "'$value'")}} }
foreach ($dir in Get-ChildItem $root -Directory) {
    $pagePath = Join-Path $dir.FullName 'page.json'
    $page = Get-Content $pagePath -Raw | ConvertFrom-Json -AsHashtable
    $page.width=1280; $page.height=720; $page.displayOption='FitToPage'
    $page.objects=@{background=@(@{properties=@{color=(Color '#F3F5F8');transparency=(Lit '0D')}})}
    $page | ConvertTo-Json -Depth 100 | Set-Content $pagePath -Encoding utf8NoBOM
    $files = @(Get-ChildItem (Join-Path $dir.FullName 'visuals') -Recurse -Filter visual.json)
    $entries = @($files | ForEach-Object { @{path=$_.FullName; data=(Get-Content $_ -Raw | ConvertFrom-Json -AsHashtable)} })
    $cards=@($entries | Where-Object {$_.data.visual.visualType -eq 'cardVisual'})
    $charts=@($entries | Where-Object {$_.data.visual.visualType -notin @('cardVisual','textbox','slicer')})
    $slicers=@($entries | Where-Object {$_.data.visual.visualType -eq 'slicer'})
    $i=0
    foreach($e in $cards) {
        $w=(1216-16*($cards.Count-1))/$cards.Count
        $e.data.position.x=32+$i*($w+16); $e.data.position.y=96
        $e.data.position.width=$w; $e.data.position.height=112; $i++
    }
    $chartWidth=if($slicers.Count){968}else{1216}
    $i=0
    foreach($e in $charts) {
        $cols=if($charts.Count -eq 1){1}else{2}
        $rows=[math]::Ceiling($charts.Count/$cols)
        $w=($chartWidth-16*($cols-1))/$cols; $h=(456-16*($rows-1))/$rows
        $e.data.position.x=32+($i%$cols)*($w+16); $e.data.position.y=232+[math]::Floor($i/$cols)*($h+16)
        $e.data.position.width=$w; $e.data.position.height=$h; $i++
    }
    $i=0
    foreach($e in $slicers) {
        $e.data.position.x=1024; $e.data.position.y=232+$i*228
        $e.data.position.width=224; $e.data.position.height=212; $i++
    }
    foreach($e in $entries) {
        $v=$e.data.visual
        if($v.visualType -eq 'textbox') {
            $e.data.position.x=32; $e.data.position.y=24; $e.data.position.width=1216; $e.data.position.height=56
            foreach($p in $v.objects.general[0].properties.paragraphs) {foreach($t in $p.textRuns){$t.textStyle=@{fontSize='24pt';fontWeight='bold';color='#202B35';fontFamily='Segoe UI'}}}
        } else {
            if(-not $v.visualContainerObjects){$v.visualContainerObjects=@{}}
            $v.visualContainerObjects.background=@(@{properties=@{color=(Color '#FFFFFF');transparency=(Lit '0D')}})
            $v.visualContainerObjects.border=@(@{properties=@{show=(Lit 'true');color=(Color '#DFE5EC');radius=(Lit '4D')}})
        }
        $e.data | ConvertTo-Json -Depth 100 | Set-Content $e.path -Encoding utf8NoBOM
    }
    if(-not ($entries | Where-Object {$_.data.visual.visualType -eq 'textbox'})) {
        $name='portfolioPageHeading'
        $target=Join-Path $dir.FullName "visuals/$name"
        New-Item $target -ItemType Directory -Force | Out-Null
        $heading=@{'$schema'='https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.8.0/schema.json';name=$name;position=@{x=32;y=24;z=0;width=1216;height=56;tabOrder=0};visual=@{visualType='textbox';objects=@{general=@(@{properties=@{paragraphs=@(@{textRuns=@(@{value=$page.displayName;textStyle=@{fontSize='24pt';fontWeight='bold';color='#202B35';fontFamily='Segoe UI'}})})}})}}}
        $heading | ConvertTo-Json -Depth 100 | Set-Content (Join-Path $target 'visual.json') -Encoding utf8NoBOM
    }
}
