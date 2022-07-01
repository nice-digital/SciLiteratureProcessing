Software to process scientific literature (titles/abstracts). The software is presented as notebooks that can be launched via Google Colab.

### Pattern Matching [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/nice-digital/SciLiteratureProcessing/blob/main/code/screen_patternmatch_regex.ipynb)

This notebook utilizes a combination of Python spaCy rule based matcher and regular expressions to create screening patterns corresponding to various subject categories and study designs. While the code was developed to categorise COVID-19 datasets, the implemented pattern matching code can screen for supported categories in any datasets.

This work is described in the following publication. Please cite this paper if you use this software in your research.   
_Sood MR, Sharp S, McFarlane E, Willans R, Hopkins K, Karpusheff J, Glen F. Managing the evidence infodemic: Automation approaches used for developing NICE COVID-19 living guidelines. medRxiv. 2022 Jan 1._



```
Copyright (c) 2022 National Institute for Health and Care Excellence (NICE)
Version: 1.0
Author: Mariam Sood 

BSD 3-Clause License

Copyright (c) 2022, National Institute for Health and Care Excellence (NICE)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
