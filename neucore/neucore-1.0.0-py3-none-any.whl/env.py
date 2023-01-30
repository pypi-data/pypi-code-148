# MIT License

# Copyright (c) 2022 Ailiverse

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

url="https://api.ailiverse.com" ## change the url

SIGN_UP_URL="{}/signUp".format(url)
SIGN_IN_URL="{}/signIn".format(url)
CREATE_MODEL_URL="{}/createModel_load".format(url)
UPLOAD_URL="{}/userUpload".format(url)
STATUS_URL="{}/status".format(url)
TRAIN_URL="{}/train".format(url)
INFER_URL="{}/infer_load".format(url)
INFER_ASYNC_URL="{}/inferAsync_load".format(url)
RESULTS_URL="{}/results".format(url)

URL_DICT = {
    "1" : { "SIGN_UP_URL" : SIGN_UP_URL, # version 1
            "SIGN_IN_URL" : SIGN_IN_URL,
            "CREATE_MODEL_URL": CREATE_MODEL_URL,
            "UPLOAD_URL": UPLOAD_URL,
            "STATUS_URL": STATUS_URL,
            "TRAIN_URL": TRAIN_URL,
            "INFER_URL": INFER_URL,
            "INFER_ASYNC_URL": INFER_ASYNC_URL,
            "RESULTS_URL": RESULTS_URL},
}
