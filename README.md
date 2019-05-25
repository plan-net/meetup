meetup
======

Meetup Demo Project.

Ensure you meet the core4os prerequisites as described in
https://core4os.readthedocs.io/en/latest/install/prereq.html.
 
Then install and run with:

    git clone https://github.com/plan-net/meetup.git
    cd meetup
    python3 -m venv .venv
    source enter_env
    pip install -U pip
    pip install .
    coco --help
    coco --job
    coco --enqueue meetup.job.MyJob
    coco --worker
    coco --app
