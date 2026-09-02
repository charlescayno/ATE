
@echo off

echo **************************************************
echo ***  Script for Generating Commit Guide        ***
echo ***       (C) 2022 Power Integrations          ***
echo **************************************************
@echo:


::======================== Author ID (HEX) ==========================
set author_id_Release=0
set author_id_jvallo=1
set author_id_rnueda=2
set author_id_ripurong=3
set author_id_csales=4
set author_id_kpangan=5

:: Update this author ID
set "author_id=%author_id_ripurong%"
REM echo author ID:	%author_id%

::======================== End of Author ID (HEX) ==========================


::======================== Git Commands  ==========================

REM Change "tokens=1-3 delims=/" to "tokens=2-4 delims=/" for USA Date structure
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set dt=%%c-%%a-%%b)
::echo %dt%


set "yy=%dt:~2,2%" & set "yyyy=%dt:~0,4%" & set "dd=%dt:~5,2%" & set "mm=%dt:~8,2%"
set "datestamp=%yy%%mm%%dd%"
::echo %datestamp%

:: Default is 7 character commit hash , gitlab use 8 characters
call git config --global log.abbrevCommit yes
call git config --global core.abbrev 8

:: Get Current branch Name 
for /f "usebackq" %%b in (`git rev-parse --abbrev-ref HEAD`) do (
	set "BranchName=%%b"
)


:: Get all Revision Count in the repository
for /f "usebackq" %%b in (`git rev-list --count --all HEAD`) do (
set "Commit_Cnt_Repo=%%b"	
)


::  gets tag from current branch
for /f "usebackq" %%b in (`git rev-parse --short master`) do (
set "Master_Tag_hash=%%b"	
)
REM echo %Master_Tag_hash%

::gets tags across all branches, not just the current branch
for /f "usebackq" %%b in (`git describe --tags %Master_Tag%`) do (
set "Master_Tag=%%b"	
)
REM echo %Master_Tag%

:: Get the total commit count on the branch
for /f "usebackq" %%b in (`git rev-list --count HEAD`) do (
	
	set "Total_Branch_Commit=%%b"
)
		
:: Get the total commit count on this branch today	
for /f "usebackq" %%b in (`git rev-list --all --count --since=midnight`) do (
set "Commit_Cnt_Today=%%b"	
)

REM echo rev is %Commit_Cnt_Today%

for /f "usebackq" %%b in (`git rev-parse --short HEAD`) do (
set "Short_Hash_Commit=%%b"	
)

:: echo %Master_Tag%
set MasterTagNo=%Master_Tag:~15,3%
REM echo %MasterTagNo%

:: echo %BranchName%
set DER_Number=%BranchName:~12,7%
REM echo %DER%

set Jira_Issue=%BranchName:~-7%
REM echo %Jira%

set /a "NextCommitCount=%Total_Branch_Commit% + 1"

@echo:
echo Commit Guide Template: 
echo PI_ATE_v01.00_%datestamp%_C%NextCommitCount%_M%MasterTagNo%_AID%author_id%_%Jira_Issue%
echo $Changes:
echo -


set line1=PI_ATE_v01.00_%datestamp%_C%NextCommitCount%_M%MasterTagNo%_AID%author_id%_%Jira_Issue%
set line2=$Changes:
set line3=-
@echo off
(
echo %line1%
echo %line2%
echo %line3%
)|clip

@echo:
echo Notes: Modify AID1 on Generated Commit Guide
::================== End of Git Commands ======================


::========================  Git  Informations   =========================
@echo:

:: Show Daily Firmware Version
echo Current Branch      :  %BranchName%
echo Total Branch Commit :  %Total_Branch_Commit%
echo Commit Count Today  :  %Commit_Cnt_Today%
echo Commit HEAD Hash    :  H-%Short_Hash_Commit%     

::========================  End of Git Information  =========================

::=====================================================================================================

REM git rev-list --count --all --since="03-28-2020 00:00" --before="03-28-2020 23:59" HEAD
REM git log --since="03-28-2020 00:00" --before="03-28-2020 23:59" --> Show all commits on a date

REM git rev-list --count HEAD					-->> This is total no of commits in a branch

REM git rev-list HEAD --count --since=1.days 	-->> This is total no of commits today

REM git rev-list --all --count --since="2020-03-31 00:00" --until="2020-03-31 23:59"						-->> This is total no of commits in all branches each day

REM git log --oneline --date=short --reverse --all --since="2020-03-31 00:00"  --until="2020-03-31 23:59"  	-->> Shows all the commit on a day, use this to retrieve from otp

REM git log --all --reverse --pretty=format:%h --since="2020-03-31 00:00" --until="2020-03-31 23:59" 		-->>Show all the commit hash in ascending order

REM git rev-list --count --since="03-31-2020 00:00" --until="2020-03-31 23:59" <revision>   				-->> This is how to get the count number of a hash or revision

REM git show -s --format=%s <hash revision>  -->> This is to show the commit message of a certain commit

REM git show-branch --no-name <hash>   -->> This is to show the commit message of a certain commit