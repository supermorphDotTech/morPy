<#
.SYNOPSIS
	This script executes the morPy framework from PowerShell.
.DESCRIPTION
	This script executes the morPy framework. In order to do it,
	the installation path of python and it's version will be
	checked.
.EXAMPLE
	Run the script
.INPUTS
	None
.OUTPUTS
	stderr & stdout to console
.NOTES
	Visit supermorph.tech on
		https://github.com/supermorphDotTech
	for more modules and other cool stuff check out the homepage
		https://www.supermorph.tech/
		
	For debugging, see the transcript created in $sTranscript
	(default is C:\Users\USERNAME\SCRIPTNAME.log).
	
	Author:			Bastian Neuwirth
	Creation Date:	30.10.2024
	Modified Date:	-
	Version:		v0.1
	
	Changelog
		v0.1
			Initial creation.
.COMPONENT
	This cmdlet is part of a Python app.
.ROLE
	This cmdlet serves the purpose of running the morPy framework from
	PowerShell for Microsoft Windows integration. It also serves
	as a Python version requirement check.
.FUNCTIONALITY
	!! LIMITATIONS !!
	Every script/module being executed from this template as the main
	process needs to have it's own unique filename disregarding of it's
	actual file path. Otherwise these scripts/modules will try to write
	the very same file.

	Due to how transcripts work in powershell, running multiple instances
	and multiple transcripts at the same time may lead to errors. The
	command Stop-Transcript will only stop the last transcript started. In
	case of multiple instances it may lead to loss of data or even file I/O
	collisions.
#>

#---------------------------------------------------
#.................[Initialisations].................
#---------------------------------------------------

#Client Name
$sClientName = $env:Computername

#User Name
$sUserName = $env:USERNAME

#User Profile
$sUserProfile = $env:USERPROFILE

#Temp folder
$sTemp = "$env:WINDIR\Temp"

#Log folder
$sLogFolder = "$sUserProfile\Documents"

#Set Error Action to Silently Continue
$ErrorActionPreference = "SilentlyContinue"

#Script Version
$sScriptVersion = "v0.1"

#Script name
$sScriptName = $MyInvocation.MyCommand.Name

#---------------------------------------------------
#..................[Declarations]...................
#---------------------------------------------------

#Path to the Python script to be executed
$sPyScript = Join-Path -Path $PSScriptRoot -ChildPath "__main__.py"

#Arguments for the Python script
$sPyArgs = ""

#Path to the Python installation
# $sPyProg = cmd /c "where python" '2>&1'
$sPyProg = Join-Path -Path $PSScriptRoot -ChildPath "\.venv-win\Scripts\Python.exe"

#Python environment is virtual
$bVenv = $true

#Minimum required Python version for the called Python app
$sPyMinVersion = "3.10.0"

#Setting TCL environment variable for Tk
if ($env:TCL_LIBRARY) {
    #Backup the existing environment variable to restore it at the end
    $bEnvTcl = $true
    $sEnvTclBackup = $env:TCL_LIBRARY
} else {
    $bEnvTcl = $false
}
$env:TCL_LIBRARY = Join-Path -Path $PSScriptRoot -ChildPath "\.venv-win\Lib\site-packages\Tcl\tcl8.6"

#Transcription (Log)
$bTranscriptEnable = $false
$sTranscript = Join-Path -Path $sLogFolder -ChildPath "$sScriptName.log"

#---------------------------------------------------
#....................[Functions]....................
#---------------------------------------------------

function fctChkPy() {
	<#
	.SYNOPSIS
		This function checks the Python installation on the host system.
		It includes the installation path and version of the installation.
	.EXAMPLE
		fctChkPy -sPyProg $sPyProg -sPyMinVersion $sPyMinVersion -bVenv $bVenv
	#>
	PARAM(
		[bool]$bTranscriptEnable,
		[string]$sPyProg,
		[string]$sPyMinVersion,
		[bool]$bVenv
	)
  
	BEGIN {
		$bErrors = $false
		$bPathCheck = $false
		$bVersionCheck = $false
		$bPyMajorVerCheck = $false
		$bPyMinorVerCheck = $false
		$bPyPatchVerCheck = $false
		$sPyVersion = python --version
		$sPyVersionPattern = 'Python (\d+\.\d+\.\d+)'
	}

	PROCESS {
		try {
			#Run Python installation check
			if ($sPyVersion -match $sPyVersionPattern) {
				#Run Python minimum version check
				$arrPyVersion = $sPyVersion.split(' ')[1].split('.')
				[int]$iPyVersionMajor = $arrPyVersion[0]
				[int]$iPyVersionMinor = $arrPyVersion[1]
				[int]$iPyVersionPatch = $arrPyVersion[2]
				$arrPyMinVersion = $sPyMinVersion.split('.')
				[int]$iPyMinVersionMajor = $arrPyMinVersion[0]
				[int]$iPyMinVersionMinor = $arrPyMinVersion[1]
				[int]$iPyMinVersionPatch = $arrPyMinVersion[2]
				#Check Major versions
				if ($iPyVersionMajor -ge $iPyMinVersionMajor) {$bPyMajorVerCheck = $true}
				#Check Minor versions
				if (($iPyVersionMajor -gt $iPyMinVersionMajor) -or
					(($iPyVersionMajor -eq $iPyMinVersionMajor) -and ($iPyVersionMinor -ge $iPyMinVersionMinor))) {$bPyMinorVerCheck = $true}
				#Check Patch versions
				if (($iPyVersionMajor -gt $iPyMinVersionMajor) -or
					($iPyVersionMajor -eq $iPyMinVersionMajor -and $iPyVersionMinor -gt $iPyMinVersionMinor) -or
					($iPyVersionMajor -eq $iPyMinVersionMajor -and $iPyVersionMinor -eq $iPyMinVersionMinor -and $iPyVersionPatch -ge $iPyMinVersionPatch)) {$bPyPatchVerCheck = $true}
				if ($bPyMajorVerCheck -and $bPyMinorVerCheck -and $bPyPatchVerCheck) {
					$bVersionCheck = $true
					#Run Python path check, if installed at all
					if (Test-Path -Path $sPyProg){
						$bPathCheck = $true
					} else {
						Write-Host -ForegroundColor red "There is an issue with the path to the Python installation."
						Write-Host -ForegroundColor yellow $sPyProg
					}
				} else {
					Write-Host -ForegroundColor red "Python version requirement not met. Visit https://www.python.org/downloads/ and install Python $sPyMinVersion or newer."
				}
			} else {
				Write-Host -ForegroundColor red "Python is not installed. You may install Python $sPyMinVersion or newer from the Microsoft Store."
			}
			#Run Python app
			if ($bVersionCheck -and $bPathCheck) {
				if ($bVenv) {
					$sVenvActivatePath = Join-Path -Path $PSScriptRoot -ChildPath "\.venv-win\Scripts\Activate.ps1"
					& $sVenvActivatePath
				}
				fctRunPy -sPyProg $sPyProg -sPyScript $sPyScript -sPyArgs $sPyArgs
			}
		}
		catch {
			$bErrors = $true
			$sErr = $_.Exception
			$sErrLine = $_.InvocationInfo.ScriptLineNumber
			$sErrMsg = $sErr.Message
			Write-Host -ForegroundColor red "ERROR at line ${sErrLine}:"
			Write-Host -ForegroundColor red "$sErrMsg"
		}
	}

	END {
		if($bErrors){
			#Stop the Script on Error
			Write-Host ""
			Write-Host -ForegroundColor red "Execution aborted."
			Read-Host "Press Enter to exit."
			if ($bTranscriptEnable) {
				Write-Host -ForegroundColor red "Review transcript $sTranscript"
				Stop-Transcript
			}
			exit
		} else {
			# Write-Host ""
			# Write-Host -ForegroundColor green "Script $sScriptName $sScriptVersion finished without errors."
			# Read-Host "Press Enter to exit."
			# return $sStringVar, $iIntVar
		}
	}
}

function fctRunPy() {
	<#
	.SYNOPSIS
		This function calls a Python (.py) file from PowerShell.
	.EXAMPLE
		fctRunPy -sPyProg $sPyProg -sPyScript $sPyScript -sPyArgs $sPyArgs
	#>
	PARAM(
		[bool]$bTranscriptEnable,
		[string]$sPyProg,
		[string]$sPyScript,
		[string]$sPyArgs
	)
  
	BEGIN {
		$bErrors = $false
	}

	PROCESS {
		try {
			$pyOutput = & $sPyProg $sPyScript $sPyArgs | ForEach-Object {
				if ($_ -match "^\s") {
					Write-Host -BackgroundColor Black -ForegroundColor DarkGray $_
				} else {
					Write-Host -BackgroundColor Black -ForegroundColor DarkYellow $_
				}
			}
			$pyOutput
		}
		catch {
			$bErrors = $true
			$sErr = $_.Exception
			$sErrLine = $_.InvocationInfo.ScriptLineNumber
			$sErrMsg = $sErr.Message
			Write-Host -ForegroundColor red "ERROR at line ${sErrLine}:"
			Write-Host -ForegroundColor red "$sErrMsg"
		}
	}

	END {
		if($bErrors){
			#Stop the Script on Error
			Write-Host ""
			Write-Host -ForegroundColor red "Execution aborted."
			Read-Host "Press Enter to exit."
			if ($bTranscriptEnable) {
				Write-Host -ForegroundColor red "Review transcript $sTranscript"
				Stop-Transcript
			}
			exit
		} else {
			# Write-Host ""
			# Write-Host -ForegroundColor green "Script $sScriptName $sScriptVersion finished without errors."
			# Read-Host "Press Enter to exit."
			# return $sStringVar, $iIntVar
		}
	}
}

#---------------------------------------------------
#..................[Transcription]...START..........
#---------------------------------------------------

if ($bTranscriptEnable) {
	if (-not (Test-Path $sLogFolder)) {
				New-Item -Path $sLogFolder -Force
			}
	Start-Transcript -Path $sTranscript
}

Write-Host -ForegroundColor DarkGreen "`n******************************************"
Write-Host -ForegroundColor DarkGreen "   $sScriptName"
Write-Host -ForegroundColor DarkGreen "   $sScriptVersion"
Write-Host -ForegroundColor DarkGreen "******************************************"

#---------------------------------------------------
#....................[Execution]....................
#---------------------------------------------------

fctChkPy -sPyProg $sPyProg -sPyMinVersion $sPyMinVersion -bVenv $bVenv

#Deactivate the virtual environment
# if ($bVenv) {
	# deactivate
# }

#Restore or delete the TCL_LIBRARY environment variable
if ($bEnvTcl) {
    $env:TCL_LIBRARY = $sEnvTclBackup
} else {
    $env:TCL_LIBRARY = $null
}

#---------------------------------------------------
#..................[Transcription]...END............
#---------------------------------------------------

if ($bTranscriptEnable) {
	Write-Host ''
	Stop-Transcript
	Write-Host ''
}

# Write-Host -ForegroundColor yellow 'App closed. Press ENTER to exit'
# Read-Host
# Write-Host ''
exit