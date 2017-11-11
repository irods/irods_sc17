#!/bin/bash
JOBS=${1-16}
for ((i=0; i<JOBS; i++)); do 
	sleep .3; rq worker -v --burst -w irodsqueue.irodsworker.IrodsWorker &
done

