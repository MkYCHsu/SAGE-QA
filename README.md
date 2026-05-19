# sage_qa

Shared-Context Agentic Graph-Enhanced Question Answering.

This version keeps the original notebook-style AutoGen behavior while making the code runnable as a small Python project. The directory name is `sage_qa`, and the Python source files live directly under `src/` without an extra `src/sage_qa/` package layer.

## Directory layout

```text
sage_qa/
├── main.py
├── serve.py
├── requirements.txt
├── agent_settings/
│   ├── common_rules.md
│   ├── planner.md
│   ├── engineer.md
│   ├── critic.md
│   ├── summarizer.md
│   ├── user_proxy.md
│   └── graphmaker.md
└── src/
    ├── app.py
    ├── config.py
    ├── core.py
    ├── prompts.py
    ├── sample_questions.py
    ├── schemas.py
    ├── agents/
    │   └── factory.py
    ├── knowledge/
    │   └── tools.py
    └── deploy/
        ├── runtime.py
        └── vllm_patch.py
```

Runtime data should stay local and should not be committed:

```text
models/
chroma/
GRAPHDATA_TSMC/
GRAPHDATA_TSMC_OUTPUT/
outputs/
```

## Required LLM endpoint

`main.py` and `serve.py` do not start the LLM model. You need to first host or connect to an OpenAI-compatible endpoint, for example a local vLLM server:

```text
http://localhost:8080/v1
```

Check the endpoint:

```bash
curl http://localhost:8080/v1/models
```

Use the returned model id as `--model`.

Example vLLM launch:

```bash
vllm serve /path/to/model \
  --host 0.0.0.0 \
  --port 8080 \
  --served-model-name llama3.3-70b
```

## Environment setup

```bash
cd sage_qa
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Or use an existing conda environment:

```bash
conda activate llm
pip install -r requirements.txt
```

## Local data setup

Expected graph data:

```text
GRAPHDATA_TSMC/
├── TSMC_SEMIKONG.pkl
└── *_chunks_clean.csv

GRAPHDATA_TSMC_OUTPUT/
└── tsmc_5b10p.graphml
```

Expected Chroma cache:

```text
chroma/
```

Expected local embedding model path:

```text
models/SEMIKONG-8b-GPTQ
```

Recommended symlink setup:

```bash
mkdir -p models
ln -s /actual/path/to/SEMIKONG-8b-GPTQ models/SEMIKONG-8b-GPTQ
ln -s /actual/path/to/chroma chroma
```

## Run one-shot QA

Sample Q1:

```bash
python main.py \
  --base-url http://localhost:8080/v1 \
  --model llama3.3-70b \
  --data-dir ./GRAPHDATA_TSMC \
  --data-dir-out ./GRAPHDATA_TSMC_OUTPUT \
  --sample-index 1
```

Custom question:

```bash
python main.py \
  --base-url http://localhost:8080/v1 \
  --model llama3.3-70b \
  --data-dir ./GRAPHDATA_TSMC \
  --data-dir-out ./GRAPHDATA_TSMC_OUTPUT \
  -q "What are the knobs that can change the uniformity in radical si-etching process?"
```

Endpoint check only:

```bash
python main.py \
  --check \
  --base-url http://localhost:8080/v1 \
  --model llama3.3-70b
```

## Serve API mode

Start the SAGE-QA API server:

```bash
python serve.py \
  --base-url http://localhost:8080/v1 \
  --model llama3.3-70b \
  --data-dir ./GRAPHDATA_TSMC \
  --data-dir-out ./GRAPHDATA_TSMC_OUTPUT \
  --port 8000
```

Call the QA endpoint:

```bash
curl -X POST http://localhost:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the knobs that can change the uniformity in radical si-etching process?"}'
```

Health check:

```bash
curl http://localhost:8000/health
```

<<<<<<< HEAD
## Notes
=======
---

## License

This project is released under the MIT License.

```text
MIT License

Copyright (c) 2026 Yu-Chuan Hsu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights    
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     
copies of the Software, and to permit persons to whom the Software is        
furnished to do so, subject to the following conditions:                     

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.                              

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
```
