from abc import ABC, abstractmethod
import numpy as np

# abstract class, should never be instantiated directly
class _PruningFunction(ABC):
    def __init__(self):
        # just a placeholder
        pass

    @abstractmethod
    def apply_pruning(self, derating_functions):
        pass

'''
No pruning is performed
'''
class PruningNone(_PruningFunction):
    def apply_pruning(self, derating_functions):
        return derating_functions

'''
Prune all the optima on the same level within the same derating radius of the best optimum of that level
'''
class PruningProximity(_PruningFunction):
    def apply_pruning(self, derating_functions):
        optima_per_level = {}
        for dfunction in derating_functions:
            dlevel = dfunction.derating_level
            dcentre_score = dfunction.score_best  # self.score_function(dfunction.centre)
            if dlevel not in optima_per_level:
                optima_per_level[dlevel] = []
            # check if other optima are already present at level dlevel
            optima_added = False
            for i, dfunction_inserted in enumerate(optima_per_level[dlevel]):
                dist = np.linalg.norm(dfunction_inserted.centre - dfunction.centre)
                if dist <= dfunction_inserted.radius or dist <= dfunction.radius:
                    if dcentre_score > dfunction_inserted.score_best:  # self.score_function(dfunction_inserted.centre):
                        optima_per_level[dlevel][i] = dfunction
                    optima_added = True
                    break
            if not optima_added:
                optima_per_level[dlevel] += [dfunction]
        optima = []
        for level in optima_per_level:
            optima += [dfunction for dfunction in optima_per_level[level]]
        return optima

'''
Prune all the optima with augmented score lesser than the cutoff value
'''
class PruningAbsScoreCutoff(_PruningFunction):
    def __init__(self, cutoff):
        self.cutoff = cutoff
        super().__init__()


    def apply_pruning(self, derating_functions):
        optima = [dfunction for dfunction in derating_functions if dfunction.score_best >= self.cutoff]
        return optima

'''
Prune all the optima with relative augmented score lesser than the cutoff percentage
'''
class PruningPercScoreCutoff(_PruningFunction):
    def __init__(self, cutoff):
        assert 0 <= cutoff <= 1, f"Cutoff value must be in [0,1], found {cutoff}"
        self.cutoff = cutoff
        super().__init__()


    def apply_pruning(self, derating_functions):
        optima_scores = sorted([dfunction.score_best for dfunction in derating_functions], reverse=True)
        score_cutoff = optima_scores[int((len(optima_scores) - 1) * self.cutoff)]
        optima = [dfunction for dfunction in derating_functions if dfunction.score_best >= score_cutoff]
        return optima