import sys

from pii_transform.api.e2e import PiiTextProcessor

# Create the object, defining the language to use and the policy
# Further customization is possible by providing a config
proc = PiiTextProcessor(lang="en", default_policy="annotate", country="gb",
                        debug=True)

# Process a text buffer and get the transformed buffer
outbuf = proc(sys.argv[1])

print(outbuf)
