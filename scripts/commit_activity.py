#!/usr/bin/env python3
"""Commit only a selected generator's owned assets; stop rather than overwrite concurrent changes."""
import argparse, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--kind',required=True,choices=['metrics','snake','contributions3d']);a=parser.parse_args()
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,capture_output=True,check=True).stdout.decode().strip()
if git('diff','--cached','--name-only'):raise RuntimeError('Unexpected staged work')
paths={'metrics':['github-metrics/base.svg','github-metrics/calendar.full.svg','github-metrics/streak.svg','github-metrics/languages.indepth.svg','github-metrics/habits.charts.svg','github-metrics/activity.svg','github-metrics/wakatime.svg'],'snake':[p.relative_to(ROOT).as_posix() for p in (ROOT/'profile-snake-contrib').glob('*.svg')],'contributions3d':[p.relative_to(ROOT).as_posix() for p in (ROOT/'profile-3d-contrib').glob('*.svg')]}[a.kind]
if a.kind=='metrics':
    paths += [p.relative_to(ROOT).as_posix() for p in (ROOT/'github-metrics').glob('*.svg') if p.stem.endswith(('-light','-dark'))]
paths=[p for p in paths if (ROOT/p).is_file()]+['assets/profile/activity-status.json']
git('add','--',*paths)
changed=git('diff','--cached','--name-only').splitlines()
if set(changed)-set(paths):raise RuntimeError('Unexpected staged paths')
if not changed:print('No generated changes.');raise SystemExit(0)
git('config','user.name','github-actions[bot]');git('config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
git('commit','-m',f'chore(profile): refresh {a.kind} assets')
# Normal push only; a concurrent owner commit causes a safe failure for the next scheduled run.
git('push','origin','HEAD:main');print(f'Updated {len(changed)} generated paths.')
