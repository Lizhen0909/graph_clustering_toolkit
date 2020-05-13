## Graph Clustering Toolkit

### Summary:
The toolkit collects many academic graph clustering programs and make them avaliable as package. Docker image is provided for easy access. 


### Installation:

Use docker is convenient as

    docker pull lizhen0909/graph_clustering_toolkit

For more information, please refer to [online document](https://lizhen0909.github.io/graph_clustering_toolkit/) for a full description

### Usage:

Start python from docker:
```
docker run -it -rm lizhen0909/graph_clustering_toolkit python
```

Run the script from the command line:
```python
import gct
from gct.dataset import random_dataset
#create a random graph use LFR generator
ds=random_dataset.generate_undirected_unweighted_random_graph_LFR(name="random_graph", \
                                       N=128, k=16, maxk=32, mu=0.2, minc=32)
# run pScan graph algorithm
pscan_clustering=gct.scan_pScan("get_start_pscan", ds)
```

See more to visit [online usage](https://lizhen0909.github.io/graph_clustering_toolkit/usage/usage.html).

### Citation:
Please cite [Comparison and Benchmark of Graph Clustering Algorithms](https://arxiv.org/abs/2005.04806) for this work.

For individual algorithms, see [Algorithms](https://lizhen0909.github.io/graph_clustering_toolkit/usage/pydoc_alg.html) for their publications.


