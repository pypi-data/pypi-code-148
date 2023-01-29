#!%PYTHON_HOME%\python.exe
# coding: utf-8
# version: python38

from yutils._import import import_numpy, import_matplotlib
from yutils.exceptions import CodeMistake, InputError
from yutils.tools import basic_plot
from yutils.ml.base.ml_base import MLObject

np = None
def _import_numpy():
    global np
    if np is None:
        np = import_numpy()


class KMeans(MLObject):
    def __init__(self, input_data, num_rand_init=30, max_iter=30, new_centroid_when_dropped=True, verbose=True):
        _import_numpy()
        super().__init__(input_data=input_data,
                         num_rand_init=num_rand_init,
                         max_iter=max_iter,
                         new_centroid_when_dropped=new_centroid_when_dropped,
                         verbose=verbose)

        self._centroids = {}
        self._new_centroid_just_created = False

    @property
    def _random_indices(self):
        indices = np.arange(self.input_data.shape[0])
        np.random.shuffle(indices)
        return indices

    @property
    def centroids(self):
        if len(self._centroids) != 1:
            raise CodeMistake("Property self._centroids has saved more than one amount of computed clusters.")
        return next(iter(self._centroids.values()))

    def compute_clusters(self, num_of_clusters):
        all_centroids_with_designations = [self._single_cluster_computation(num_of_clusters, i)
                                           for i in range(self.num_rand_init)]
        self._verbose_print("")

        centroids, centroid_designations = self._get_best_centroids(all_centroids_with_designations)

        self._centroids[num_of_clusters] = (centroids, centroid_designations)
        return centroids, centroid_designations

    def _single_cluster_computation(self, num_of_clusters, randomization_number):
        centroids = self._init_centroids(num_of_clusters)
        centroid_designations = np.zeros(self.input_data.shape[0])
        for iteration in range(self.max_iter):
            self._verbose_print(f"\rRandomization #{randomization_number + 1} ~ "
                                f"K-Means Iteration #{iteration + 1}", no_end=True)
            new_centroid_designations = self._find_closest_centroid(centroids)

            changed = np.any(new_centroid_designations != centroid_designations)
            if not changed:
                break
            centroid_designations = new_centroid_designations

            centroids = self._move_centroids(centroid_designations, num_of_clusters)

        # If loop was stopped because self.max_iter was reached (and not because of break),
        # or if a new centroid has just been created, refresh centroid designation
        if changed or self._new_centroid_just_created:
            centroid_designations = self._find_closest_centroid(centroids)

        return centroids, centroid_designations

    def _get_best_centroids(self, all_centroids_with_designations):
        if self.num_rand_init > 1:
            costs = np.array([self._j_cost_function(c, cd) for c, cd in all_centroids_with_designations])
            index = np.argmin(costs)
        else:
            index = 0

        return all_centroids_with_designations[index]

    def _init_centroids(self, num_of_clusters):
        return self.input_data[self._random_indices[:num_of_clusters]]

    def _find_closest_centroid(self, centroids):
        closest_centroid_ind = []
        for example in self.input_data:
            distances = np.array([self._distance(example, centroid) for centroid in centroids])
            closest_centroid_ind.append(np.argmin(distances))
        return np.array(closest_centroid_ind)

    def _move_centroids(self, centroid_designations, num_of_clusters):
        self._new_centroid_just_created = False

        centroids = []
        for group in np.unique(centroid_designations):
            examples = self.input_data[centroid_designations == group]
            centroids.append(np.mean(examples, axis=0))

        self._add_new_centroids(centroids, num_of_clusters - len(centroids))

        return np.array(centroids)

    def _add_new_centroids(self, centroids, num_missing_centroids):
        if not num_missing_centroids:
            return

        self._verbose_print("")
        self._verbose_print(f"{num_missing_centroids} centroid{'s' * (num_missing_centroids > 1)} dropped! ",
                            no_end=self.new_centroid_when_dropped)
        if self.new_centroid_when_dropped:
            self._verbose_print(f"Randomizing {num_missing_centroids} new "
                                f"centroid{'s' * (num_missing_centroids > 1)}")
            for index in self._random_indices[:num_missing_centroids]:
                centroids.append(self.input_data[index])
            self._new_centroid_just_created = True

    @staticmethod
    def _distance(x, y):
        return sum((x - y) ** 2)

    def _j_cost_function(self, centroids, centroid_designations):
        distances = np.array([self._distance(example,
                                             centroids[int(centroid_designations[i])])
                              for i, example in enumerate(self.input_data)])
        return np.mean(distances)

    def plot_clusters(self, centroids, centroid_designations):
        plot_clusters(self.input_data, centroids, centroid_designations)

    def plot_elbow_graph(self, max_k=10):
        ks = np.arange(1, max_k + 1)
        costs = []
        for k in ks:
            centroids, centroid_designations = self.compute_clusters(k)
            costs.append(self._j_cost_function(centroids, centroid_designations))
        costs = np.array(costs)

        basic_plot(ks, costs, title='K-Means Elbow Graph', xlabel='Num of Clusters', ylabel='Cost')


def plot_clusters(all_data, centroids, centroid_designation):
    _import_numpy()
    plt = import_matplotlib()

    if all_data.shape[1] != 2 or centroids.shape[1] != 2:
        raise InputError("To plot centroids, you must have 2 dimensional data!")

    colors = ['b', 'r', 'g', 'orange', 'y', 'c', 'm']
    groups = np.unique(centroid_designation)
    if len(groups) > len(colors):
        colors = [f"C{i}" for i in range(len(groups))]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i, group in enumerate(groups):
        group_data = all_data[centroid_designation == group]
        ax.scatter(group_data[:, 0], group_data[:, 1], c=colors[i], marker='.')
        ax.scatter(centroids[group, 0], centroids[group, 1], c='k', marker='X')

    plt.show()
