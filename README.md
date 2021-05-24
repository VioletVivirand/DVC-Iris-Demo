This is a simple demo for [DVC](https://dvc.org).

> [UPDATE] In 2021, we can use [DAGsHub](https://dagshub.com/) to integrate Git & DVC & MLFlow on a same platform! Go check the [getting-started page of DAGsHub](https://dagshub.com/get-started) and give it a try.

## Step by step

### Step 0: Install DVC Package

```bash
# Install DVC into system
$ pip install dvc[all]

# Create a Virtualenv to install necessary packages
$ pipenv shell
$ pipenv install numpy pandas scikit-learn
```

### Step 1: Initialize Project

```bash
# Initialize Git Repo
$ git init

# Initialize DVC Repo
$ dvc init

# When initialize DVC repo,
# the basic things are already added to index,
# so we just need to commit
$ git commit -m "Initialize DVC project"
```

### Step 2: Add a remote storage

```bash
# Create a new directory and assign as a local storage
$ mkdir ~/DVC-Iris-Storage

# Add a local remote for demo usage
$ dvc remote add -d myremote ~/DVC-Iris-Storage

# The config file at "/.dvc/config" gets updated, commit it
$ git commit .dvc/config -m "Configure local remote pipeline"
```

### Step 3: Fetch Data Pipeline

```bash
$ mkdir data

# Add script to fetch data
$ mkdir src
$ vi src/getdata.sh
$ chmod +x src/getdata.sh
$ git add src/getdata.sh
$ git commit -m "Add script to fetch data"

# Build a pipeline to fetch data from source
$ dvc run -f getdata.dvc \
          -d src/getdata.sh \
          -o data/iris.csv \
          src/getdata.sh data/iris.csv

# Follow the instruction to commit DVC files
$ git add data/.gitignore getdata.dvc
$ git commit -m "Configure dataset fetching pipeline"

# Push data to remote storage
$ dvc push
```

### Step 4: Featurize

```bash
# Add "/data/features" directory
$ mkdir data/features

# Part 1: Add featurize code
$ vi src/featurize.py
$ git add src/featurize.py
$ git commit -m "Add featurize code"

# Build a featurize pipeline
$ dvc run -f featurize.dvc \
          -d src/featurize.py -d data/iris.csv \
          -o data/features/iris.h5 \
          python src/featurize.py \
          data/iris.csv \
          data/features/iris.h5

# Follow the instruction to commit DVC files
$ git add featurize.dvc data/features/.gitignore
$ git commit -m "Configure featurization pipeline"

# Push data to remote storage
$ dvc push
```

```bash
# Part 2: Split train and test data
$ vi src/split.py
$ git add src/split.py
$ git commit -m "Add code to split data"

# Build a pipeline to split data
$ dvc run -f split.dvc \
          -d src/split.py -d data/features/iris.h5 \
          -o data/features/train.h5 -o data/features/test.h5 \
          python src/split.py \
          data/features/iris.h5 \
          data/features/
# Follow the instruction to commit DVC files
$ git add split.dvc data/features/.gitignore
$ git commit -m "Configure train test split pipeline"

# Push data to remote storage
$ dvc push
```

### Step 5: Training

```bash
# Add "/data/model" directory
$ mkdir data/model

# Add training code
$ mkdir src
$ vi src/train.py
$ git add src/train.py
$ git commit -m "Add training code"

# Build a training pipeline
$ dvc run -f train.dvc \
          -d src/train.py -d data/features/train.h5 \
          -o data/model/model.joblib \
          python src/train.py \
          data/features/train.h5 \
          data/model/
# Follow the instruction to commit DVC files
$ git add data/model/.gitignore train.dvc
$ git commit -m "Configure training pipeline"

# Push data to remote storage
$ dvc push
```

### Step 6: Evaluating

```bash
# Add evaluating code
$ vi src/evaluate.py
$ git add src/evaluate.py
$ git commit -m "Add evaluation code"

# Build a evaluating pipeline
$ dvc run -f evaluate.dvc \
          -d src/evaluate.py \
          -d data/model/model.joblib \
          -d data/features/test.h5 \
          -M score.metric \
          python src/evaluate.py \
          data/model/model.joblib \
          data/features/test.h5 \
          score.metric

# Follow the instruction to commit DVC files
$ git add evaluate.dvc
# And don't forget to commit metric file manually!
$ git add score.metric
$ git commit -m "Configure evaluation pipeline"

# Push data to remote storage
$ dvc push

# Tag this experiment
$ git tag -a "baseline-experiment" \
          -m "Baseline experiment evaluation"
```

### Step 7: Make another experiment

```bash
# Modify training code, modify the parameters
$ vi src/train.py
$ git add src/train.py
$ git commit -m "Modify training code"

# Reproduce the experiment
$ dvc repro evaluate.dvc

# Follow the instruction to commit DVC files
$ git add evaluate.dvc train.dvc getdata.dvc
# And don't forget to commit metric file manually!
$ git add score.metric
$ git commit -m "Configure evaluation #2"

# Push data to remote storage
$ dvc push

# Tag this experiment
$ git tag -a "#2-experiment" \
          -m "#2 experiment evaluation"
```

### View the results

```bash
# Visualize pipeline
$ dvc pipeline show --ascii evaluate.dvc
# Visualize pipeline with outputs
$ dvc pipeline show --ascii evaluate.dvc --outs
# Visualize pipeline with commands
$ dvc pipeline show --ascii evaluate.dvc --commands

# Show metric
$ dvc metrics show
# Show all metrics
$ dvc metrics show -a
# Show all metrics with tag
$ dvc metrics show -T
```
