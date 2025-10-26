# Rename EDFlow AI to EDFlow AI across all files
$files = Get-ChildItem -Recurse -File -Include *.py,*.md,*.yml,*.yaml,*.json,*.txt,*.ts,*.tsx,*.js,*.jsx,*.html,*.css,*.sh,*.example,*.production

foreach ($file in $files) {
    try {
        $content = Get-Content $file.FullName -Raw -ErrorAction Stop
        if ($content -match 'EDFlow AI') {
            $newContent = $content -replace 'EDFlow AI', 'EDFlow AI'
            Set-Content -Path $file.FullName -Value $newContent -NoNewline
            Write-Host "Updated: $($file.FullName)"
        }
    }
    catch {
        Write-Host "Skipped: $($file.FullName) - $($_.Exception.Message)"
    }
}

Write-Host "`nRename complete!"