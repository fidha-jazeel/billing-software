Set objArgs = WScript.Arguments
If objArgs.Count < 2 Then
    WScript.Echo "Usage: update_iss_version.vbs <version> <iss_file>"
    WScript.Quit 1
End If

version = objArgs(0)
issFile = objArgs(1)

Set fso = CreateObject("Scripting.FileSystemObject")
Set inputFile = fso.OpenTextFile(issFile, 1)
content = inputFile.ReadAll
inputFile.Close

' Replace the version line
Set re = New RegExp
re.Pattern = "#define MyAppVersion "".*"""
re.Global = True
content = re.Replace(content, "#define MyAppVersion """ & version & """")

Set outputFile = fso.OpenTextFile(issFile, 2)
outputFile.Write content
outputFile.Close

WScript.Echo "Version updated to " & version
