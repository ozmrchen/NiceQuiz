
### How to combine code files into one for LLMs

Windows
```
"# filename: main.py" | Out-File combined_code.txt
Get-Content main.py | Out-File -Append combined_code.txt
"# filename: quiz_bank.py" | Out-File -Append combined_code.txt
Get-Content quiz_bank.py | Out-File -Append combined_code.txt

```

Mac
```
(printf '# filename: main.py\n'; cat main.py; printf '\n# filename: quiz_bank.py\n'; cat quiz_bank.py) > combined_code.txt
```