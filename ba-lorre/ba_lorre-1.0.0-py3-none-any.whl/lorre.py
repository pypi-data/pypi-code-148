#!/usr/bin/env python3

"""
Code developed by Luca Baronti (lbaronti[at]gmail.com)
"""
import signal, logging
from collections.abc import Callable
import numpy as np
from bees_algorithm import BeesAlgorithm, Bee
import benchmark_functions as bf
from . import pruning_functions as pf

DEFAULT_LORRE_LOG_DIR = '/tmp/LORRE_logs'

class LORRE_Bee(Bee):
    def __init__(self, range_min, range_max, ttl, ngh, level, isForager=False, centre=None):
        super().__init__(range_min, range_max, ttl, ngh, isForager, centre)
        self.worst_solutions = []
        self.good_solutions = []  # history of solutions
        self.level = level
        self.values = np.array(self.values)

    def generateForager(self):
        b = LORRE_Bee(self.range_min, self.range_max, self.ttl, self.ngh, self.level, isForager=True, centre=self.values)
        b.worst_solutions = self.worst_solutions
        b.good_solutions = self.good_solutions
        return b

    def __le__(self, other):
        return self.score <= other.score

class DeratingFunction:
    def __init__(self, final_solution, derating_level, radius_selection_criterion: str= 'median', type='flat'):
        assert radius_selection_criterion in ['median', 'topological']
        assert type in ['flat', 'linear']
        self.derating_level = derating_level
        self.type = type
        selected_worst_solution = self.findReferenceWorstSolution(final_solution, radius_selection_criterion)
        self.score_worst = selected_worst_solution.score
        self.score_best  = final_solution.score
        self.centre = np.array(final_solution.values)
        self.radius = np.linalg.norm(self.centre - selected_worst_solution.values)

    def __str__(self):
        return f"level: {self.derating_level} centre: {self.centre} radius: {self.radius} score (w/b): ({self.score}/{self.score_best})"

    def findReferenceWorstSolution(self, final_solution, radius_selection_criterion):
        # sort the worst solutions according their distance with the final solution
        worst_solutions = [w for w in final_solution.worst_solutions]
        assert len(worst_solutions) > 0
        worst_solutions.sort(key=lambda w: np.linalg.norm(final_solution.values - w.values))

        if radius_selection_criterion == 'median':
            selected_worst_solution = worst_solutions[(len(worst_solutions) - 1) // 2]
        elif radius_selection_criterion == 'topological':
            raise NotImplementedError(f"Topological radius selection criterion not implemented yet!")
        else:
            raise NotImplementedError(f"Radius selection criterion '{radius_selection_criterion}' not implemented yet!")

        return selected_worst_solution

    def getScoreForSolution(self, solution, distance=None):
        if self.type == 'flat':
            return self.score_worst
        elif self.type == 'linear':
            if distance is None:
                distance = np.linalg.norm(solution.values - self.centre)
            assert distance <= self.radius, (distance, self.radius)
            penalty_term = abs(self.score_worst)*0.01*(1.0 - distance/self.radius)
            return self.score_worst - penalty_term
        else:
            raise ValueError(f"Unknown derating type {self.type}")

class LORRE(BeesAlgorithm):
    """
    Derating position is a list of indexes of the genome values which need to be considered for the derating function.
    """
    def __init__(self, score_function: Callable[[list], float], range_min: list, range_max: list, nb: int=5, nrb: int=10, stlim:int=10,
                 initial_ngh=None, shrink_factor: float=.2, derating_radius_selection_criterion: str='median', derating_type: str='linear'):
        self.derating_functions = []
        self.derating_type = derating_type
        self.derating_radius_selection_criterion = derating_radius_selection_criterion
        super().__init__(score_function, range_min, range_max, ns=0, nb=nb, ne=0, nrb=nrb, nre=0,
                            stlim=stlim, initial_ngh=initial_ngh, shrink_factor=shrink_factor,
                            useSimplifiedParameters=True)

    def _generateScout(self):
        bee = LORRE_Bee(self.range_min, self.range_max, self.stlim, self.initial_ngh,
                        level=len(self.derating_functions), isForager=False, centre=None)
        bee.score = self.augmented_score_function(bee)
        return bee

    def _generateForager(self, site):
        bee = site.generateForager()
        bee.score = self.augmented_score_function(bee)
        return bee

    def _generateForagers(self, site, n_foragers):
        foragers = np.array([self._generateForager(site) for _ in range(n_foragers)])
        worst_forager = np.min(foragers)
        site.worst_solutions += [worst_forager]
        best_forager = np.max(foragers)
        # we need to recompute the score because new derating functions may have been added to the region
        site.score = self.augmented_score_function(site)
        if site.score > best_forager.score:
            site.good_solutions += [site]
        else:
            site.good_solutions += [best_forager]
        return foragers

    # implementation of eq (12) in the paper
    def augmented_score_function(self, solution):
        # find the closest derating function centre to the solution
        closest_idx, closest_distance = None, None # they can stay None if no derating functions are present
        for i, df in enumerate(self.derating_functions):
            if solution.level < df.derating_level:
                # derating function df has been created after the site
                continue
            d = np.linalg.norm(solution.values - df.centre)
            if closest_idx is None or closest_distance > d:
                closest_idx = i
                closest_distance = d
        if closest_distance is not None and closest_distance <= self.derating_functions[closest_idx].radius:
            return self.derating_functions[closest_idx].getScoreForSolution(solution, closest_distance)
        return self.score_function(solution.values)

    def _generate_solution_at_position(self, position):
        bee = self._generateScout()
        bee.values = position
        bee.score = self.augmented_score_function(bee)
        return bee

    def performSingleStep(self):
        super(LORRE, self).performSingleStep()
        for site in self.current_sites:
            if site.ttl == 0:
                self.derating_functions += [DeratingFunction(site, site.level, radius_selection_criterion=self.derating_radius_selection_criterion, type=self.derating_type)]

    def visualize_iteration_steps(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logging.error("In order to visualise the steps of the LORRE Algorithm, the following libraries are required: numpy, mpl_toolkits and matplotlib")
            return

        self.keep_bees_trace = True
        if len(self.range_min) != 2 or len(self.range_max)!=2:
            logging.error("In order to visualise the steps of the LORRE Algorithm the score function must be defined in 2 dimensions")
        x = np.linspace(self.range_min[0], self.range_max[0], 50)
        y = np.linspace(self.range_min[1], self.range_max[1], 50)

        p_size = (self.range_max[0] - self.range_min[0])*.01
        fig = plt.figure()
        iteration = 0
        ax = plt.axes(projection='3d')
        X, Y = np.meshgrid(x, y)
        Z = np.asarray([[self._generate_solution_at_position([X[i][j], Y[i][j]]).score
                            for j in range(len(X[i]))] for i in range(len(X))])
        function_surface = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.view_init(60, 35)
        n_derating_functions = 0
        signal.signal(signal.SIGINT, signal.default_int_handler)
        try:
            while True:
                iteration += 1
                self.performSingleStep()
                if len(self.derating_functions) > n_derating_functions:
                    n_derating_functions = len(self.derating_functions)
                    Z = np.asarray([[self._generate_solution_at_position([X[i][j], Y[i][j]]).score
                                        for j in range(len(X[i]))] for i in range(len(X))])
                    function_surface.remove()
                    function_surface = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=.3)

                fig.canvas.manager.set_window_title("Bees Algorithm Iteration "+str(iteration))
                fig.suptitle("Best Solution "+str(self.best_solution))
                points_x, points_y = [], []
                colors, sizes = [], []
                for b in self.to_save_best_sites:
                    points_x += [b.values[0]]
                    points_y += [b.values[1]]
                    colors   += ['blue']
                    sizes    += [p_size*2.0]
                for fs in self.to_save_foragers:
                    for f in fs:
                        points_x += [f.values[0]]
                        points_y += [f.values[1]]
                        colors   += ['purple']
                        sizes    += [p_size]
                for dfunction in self.derating_functions:
                    points_x += [dfunction.centre[0]]
                    points_y += [dfunction.centre[1]]
                    colors   += ['red']
                    sizes    += [p_size]
                points_z = [self._generate_solution_at_position([points_x[i], points_y[i]]).score
                               for i in range(len(points_x))]
                points = ax.scatter(points_x, points_y, points_z, c=colors, s=sizes)
                fig.canvas.draw()
                fig.canvas.flush_events()
                fig.show()
                input(f"Iteration {iteration} done, press any key to continue..")
                points.remove()
        except KeyboardInterrupt:
            print()
            print(f'Training terminated by the user at iteration {iteration}')

    '''
    Pruning types:
     - none: no optima pruning is performed;
     - proximity: optima on the same level within the same derating radius of the best optimum of that level are discarded
    '''
    def getFoundOptima(self, pruning_functions: list=[], return_optima_level: bool=False, verbose: bool=True):
        assert type(pruning_functions) == list
        optima = self.derating_functions
        for pruning_function in pruning_functions:
            assert isinstance(pruning_function, pf._PruningFunction)
            optima = pruning_function.apply_pruning(optima)

        if verbose:
            print(f"From {len(self.derating_functions)} optima {len(optima)} ({len(optima)/len(self.derating_functions):.2%}) are returned")
        if return_optima_level:
            return [(dfunction.centre, dfunction.derating_level) for dfunction in optima]
        else:
            return [dfunction.centre for dfunction in optima]

    def showFoundOptima(self, on_augmented_function=False, pruning_functions=[]):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logging.error("In order to visualise the steps of the LORRE Algorithm, the following libraries are required: numpy, mpl_toolkits and matplotlib")
            return
        if len(self.range_min) != 2 or len(self.range_max)!=2:
            logging.error("In order to visualise the optima found by LORRE Algorithm on the score function, it must be defined in 2 dimensions")
        x = np.linspace(self.range_min[0], self.range_max[0], 50)
        y = np.linspace(self.range_min[1], self.range_max[1], 50)

        p_size = (self.range_max[0] - self.range_min[0]) * .01
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        X, Y = np.meshgrid(x, y)
        if on_augmented_function:
            Z = np.asarray([[self._generate_solution_at_position([X[i][j], Y[i][j]]).score
                             for j in range(len(X[i]))] for i in range(len(X))])
        else:
            Z = np.asarray([[self.score_function([X[i][j], Y[i][j]])
                             for j in range(len(X[i]))] for i in range(len(X))])
        function_surface = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none', alpha=.3)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.view_init(60, 35)
        points_x, points_y = [], []
        optima = self.getFoundOptima(pruning_functions=pruning_functions)
        for optimum in optima:
            points_x += [optimum[0]]
            points_y += [optimum[1]]
        colors, sizes = ['red']*len(optima), [p_size*2.0]*len(optima)

        if on_augmented_function:
            points_z = [self._generate_solution_at_position([points_x[i], points_y[i]]).score
                       for i in range(len(points_x))]
        else:
            points_z = [self.score_function([points_x[i], points_y[i]])
                       for i in range(len(points_x))]
        ax.scatter(points_x, points_y, points_z, c=colors, s=sizes)
        plt.show()

    def showOptimaScoreHistogram(self, normalize=True, on_augmented_function=False, pruning_functions=[], verbose=False):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            logging.error("In order to visualise the steps of the LORRE Algorithm, the following libraries are required: numpy, mpl_toolkits and matplotlib")
            return
        optima = self.getFoundOptima(pruning_functions=pruning_functions, verbose=verbose)
        if on_augmented_function:
            optima_scores = np.array([self._generate_solution_at_position(optimum).score for optimum in optima])
        else:
            optima_scores = np.array([self.score_function(optimum) for optimum in optima])
        plt.hist(optima_scores, min(200, len(optima_scores)//5), density=normalize, cumulative=True)
        percentile_cuts = np.array([0.05, 0.25, 0.5, 0.75, 0.95])
        percentiles = np.percentile(optima_scores, percentile_cuts*100)
        for i, val in enumerate(percentiles):
            bar_height = min(.97, percentile_cuts[i]*1.15)
            plt.axvline(val, ymax=bar_height, linestyle=":", color='red')
            plt.text(val - .1, bar_height, f"{percentile_cuts[i]:.0%}", color='red')
        plt.grid(True)
        plt.title('Cumulative optima scores distribution')
        plt.xlabel('score')
        if normalize:
            plt.ylabel('% optima with score >= x')
        else:
            plt.ylabel('# optima with score >= x')
        plt.show()


if __name__ == "__main__":
    np.random.seed(43)
    from computational_stopwatch import Stopwatch
    b_func = bf.Schwefel(n_dimensions=2, opposite=True)
    lowerbound, upperbound = b_func.suggested_bounds()
    alg = LORRE(b_func,
              lowerbound, upperbound,
              nb=5, nrb=20,
              stlim=5, derating_type='linear')
    print(f"Function Schwefel (expected optimum: {b_func.maximum()})")
    # alg.visualize_iteration_steps()
    with Stopwatch('computation'):
        it, score = alg.performFullOptimisation(max_iteration=100,
                                                max_score=b_func.maximum().score - 1e-3)
    print("Iteration:", it, "score:", score)
    alg.showFoundOptima(pruning_functions=[pf.PruningProximity(), pf.PruningPercScoreCutoff(cutoff=.5)])
    # alg.showOptimaScoreHistogram()