# Homework 12.  NLP and Speech

Due: beginning of week 13.

Train [Conformer-Transducer](https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/models.html#conformer-transducer) BPE *Small* on LibriSpeech from scratch for 10-20 epochs.  Note that Nemo has a [script](https://github.com/NVIDIA/NeMo/blob/main/scripts/dataset_processing/get_librispeech_data.py) for downloading and processing librispeech automatically, so please use it.

Notes:
* You will obviously need to provision a VM in AWS to work on this.
* The config file for all Conformer Transducer BPE models is [here](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/conf/conformer/conformer_transducer_bpe.yaml).  It's large by default so you'll have to set it to small instead (see the header inside the file)
* The script to train the model is [here](https://github.com/NVIDIA/NeMo/blob/main/examples/asr/asr_transducer/speech_to_text_rnnt_bpe.py)
* There is a pre-trained checkpoint [here](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/stt_en_conformer_transducer_small) so that you can compare your work (and model config and params) against it.

Credit / nocredit only.  Please spend time on your final projects!!
