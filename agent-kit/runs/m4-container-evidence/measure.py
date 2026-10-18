import json,platform,resource,subprocess,sys,time
from pathlib import Path
runs=[]
for i in range(5):
 start=time.perf_counter()
 result=subprocess.run([sys.executable,'-m','engine.main'],capture_output=True,text=True)
 runs.append({'seconds':time.perf_counter()-start,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
 if result.returncode:break
peak=Path('/sys/fs/cgroup/memory.peak')
report={'platform':platform.platform(),'python':platform.python_version(),'runs':runs,'max_child_rss_bytes':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss*1024,'cgroup_memory_peak_bytes':int(peak.read_text()) if peak.exists() else None,'protocol':'Five fresh Python entrypoint processes, each processing all three supplied tasks. Wall includes interpreter/import/engine/render/output. OS caches not cleared. RSS is peak child process; cgroup memory includes page cache and all container processes.'}
Path('/app/output/resources.json').write_text(json.dumps(report,indent=2)+'\n')
sys.exit(int(any(r['exit_code'] for r in runs)))
