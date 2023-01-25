import networkx as nx
import time
import numpy as np
import copy
import uuid
import pint
from concurrent.futures import ThreadPoolExecutor
import threading
from simunetcore import exception

class Waveform(object):
    """Waveform class."""

    # Threadingo lock for non threadsafe models in Jacobi mode
    lock = threading.Lock()

    def __init__(
            self, models, edges, var_map,
            simulation_id=uuid.uuid4()):     
        """
        Creates a new Waveform relaxation object.

        Parameters
        ----------
        models : dict
            The dictionary of models.
        edges : list
            The edges (adjacencies) of the flowsheet.
        var_map : list 
            The variable map of the `edges`.
        simulation_id : uuid, optional
            The unique id of the Waveform object.
 
        """
         
        # Store models, adjacent list and var map
        self.tag = None
        self.models = models
        self.edges = edges
        self.var_map = var_map
        self.simulation_id = simulation_id
        self.compute_kwargs = {}
         
        # Create the unit registry
        self.units = pint.UnitRegistry()
        
        # Retrieve the compute order
        self.order = list(self.compute_order())

        # Number overall iterations
        self.num_iter_all = 0
        self.num_iter_used = 0
        self.num_converged_frames = 0
        self.num_restarted_frames = 0
        self.num_canceled_frames = 0
        
        # Statistics
        self.duration = 0
        self.statistics = []
        
        # List of the result frames and convergence progress
        self.frames = []
        self.convergence = []

        # Callbacks
        self.on_simulation_started = None
        self.on_frame_finished = None
        self.on_simulation_finished = None
    
    def check_var_map(self):
        """
        Checks the wether the var_map conatains incompatible mappings.
        Returns the list of incompaible mappings.

        Returns
        -------
        result : list
            A list containing the incompatible mappings.
            The elements of the result list are lists containing 
            the following elements:
            [
                model_id, u_id, var_id, dest_unit, 
                src_model_id, src_var_id, src_unit
            ]

            dest_model_id:
                The destination model id. 
            dest_u_id:
                The destination input id. 
            dest_var_id:
                The destination var id. 
            dest_unit:
                The destination unit. 
            src_model_id:
                The source model id. 
            src_var_id:
                The source var id. 
            src_unit:
                The source unit.
 
        """
       
        result = []
        # Loop through all models
        for model_id in self.models:
            model = self.models[model_id]
            # Loop through all inputs of the model
            for u_id in model.u:
                # Loop through all variables of the input
                for var_id in model.u[u_id]["vars"]:
                    # Retrieve the source model id and the 
                    # source variable name from the var map
                    src_model_id, src_var_id = self.var_map[model_id][u_id][var_id]
                    
                    # Retrieve the source unit
                    src_unit = self.models[src_model_id].vars[src_var_id]["unit"]
                    
                    # Retrieve the destination unit and convert
                    dest_unit = model.vars[var_id]["unit"]
                    
                    # Check the compatibility of the untis
                    if self.units[src_unit].is_compatible_with(dest_unit) == False:
                        # Append error to the result list
                        result.append([
                            model_id, u_id, var_id, dest_unit, 
                            src_model_id, src_var_id, src_unit])
        # Return the result
        return result
    
    def compute_connectivity(self):
        """
        Computes the connectivity of the floswheet (given by edges).
        Returns the node connectivity of the underlying directed graph.

        Returns
        -------
        connectctivity : int
            The node connectivity of the underlying directed graph.

        See Also
        --------
        networkx library : simunet uses networkx for graph algorithms.

        """

        # Create an undirected networkx graph
        graph = nx.Graph(self.edges)
        # Compute the connectctivity
        connectctivity = nx.node_connectivity(graph)
        # Return the connectivity
        return connectctivity


    def compute_order(self, include_cycles=False):
        """
        Returns the computation order of the models.

        Returns
        -------
        result : list
            The computation order of the models.
            [M1, M2, M3, ...]

        Parameters
        ----------
        include_cycles: bool, optional
            Sets wether the function should also 
            return the cycles for each model.
            [(M1 [M3, M5, ...]), M2 [], ...]

        See Also
        --------
        networkx library : simunet uses networkx for graph algorithms.

        """
       
        # Create a networkx graph
        graph = nx.DiGraph(self.edges)
        # loop until all nodes have been processed
        while len(graph.nodes()) > 0:
            # Get min of the indegree sequence
            _, next_node = min(
                [(degree, node) for node, degree in graph.in_degree()])
            # Yield the node with the minimal in degree
            if include_cycles:
                yield (next_node, list(graph.predecessors(next_node)))
            else:
                yield next_node
            # Remove the node
            graph.remove_node(next_node)

    def compute_cycles(self):
        """
        Returns the cycles in the flowsheet.

        Returns
        -------
        result : list
            The cycles for each model in the flowsheet.
            [(M1 [M3, M5, ...]), M2 [], ...]

        See Also
        --------
        networkx library : simunet uses networkx for graph algorithms.
 
        """
       
        # Create a networkx graph
        graph = nx.DiGraph(self.edges)
        # loop until all nodes have been processed
        while len(graph.nodes()) > 0:
            # Get min of the indegree sequence
            _, next_node = min(
                [(degree, node) for node, degree in graph.in_degree()])
            # Yield the next node
            for item in graph.predecessors(next_node):
                yield (item, next_node)
            # Remove the node
            graph.remove_node(next_node)

    def prepare_model_coupling(self, old_state, model_id, t_frame):
        """
        Prepares the model coupling.

        Parameters
        ----------
        old_state : dict
            The previous state of the model dictionary. 
        model_id : str
            The id of the model (key in the model dict). 
        t_frame : list
            The time frame for which the coupling should prepared. 

        Raises
        ------
        `CouplingError` if something went wrong.

        """
       
        try:
            # Prepare coupling vars
            model = self.models[model_id]
            for u_id in model.u:
                # Loop through all variables of the input
                for var_id in model.u[u_id]["vars"]:
                    # Retrieve the source model id and 
                    # the source variable name from the var map
                    src_model_id, src_var_id = self.var_map[model_id][u_id][var_id]

                    # Retrieve the source unit, destination unit and source value
                    src_unit = old_state[src_model_id].vars[src_var_id]["unit"]
                    dest_unit = model.vars[var_id]["unit"]
                    src_value = old_state[src_model_id].get_var(src_var_id, t_frame)
                    dest_value = src_value

                    # Convert only if units are different
                    if src_unit != dest_unit:
                        # Combine value with unit
                        value = src_value * self.units(src_unit)
                        # Convert and retrieve the magnitude
                        dest_value = value.to(dest_unit).magnitude

                    # Set the input for the model
                    model.set_var(var_id, dest_value)

            # Finally set the new time frame
            model.set_t(t_frame)
            
        except:
            # Raise exception
            raise exception.CouplingError(model.name, model_id, u_id)
                
    def prepare_result(self, t_out):
        """
        Prepares the aggregated result by iterating 
        over all segments and aggregating the results 
        for all models and all state varaiables.

        Parameters
        ----------
        t_out : list
            The time frame of the aggregated result. 

        """
       
        # Prepare the aggregated result of the frames
        self.models = copy.deepcopy(self.frames[1])

        for model_id in self.models:
            # Get union of u and y vars
            var_list = list(
                self.models[model_id].get_u_vars() | 
                self.models[model_id].get_y_vars())

            # Merge frames
            for frame in self.frames[2:]:
                # Merge time frames
                self.models[model_id].t += frame[model_id].t[1:]
                # Merge vars
                for var_id in var_list:
                    self.models[model_id].vars[var_id]["value"] += \
                        frame[model_id].vars[var_id]["value"][1:]

            # Interpolate to desired output time frame
            if t_out is not None:
                for var_id in var_list:
                    self.models[model_id].vars[var_id]["value"] = np.interp(
                        t_out,
                        self.models[model_id].t,
                        self.models[model_id].vars[var_id]["value"]).tolist()
                # Store the time frame as list    
                if isinstance(t_out, np.ndarray):
                    self.models[model_id].t = t_out.tolist()
                else:
                    self.models[model_id].t = t_out

    def compute_convergence(self, new_state, old_state, t_frame):
        """
        Computes the convergence between two iterations.

        Parameters
        ----------
        new_state : dict
            The new state of the model dictionary. 
        old_state : dict
            The previous state of the model dictionary. 
        t_frame : list
            The time frame for the convergence testd. 

        Returns
        -------
        convergence: list
            A list containing the result 
            of the convergence test for each model. 
            [
                [error, converged, model_id, var_id],
                [error, converged, model_id, var_id],
                ...
            ]

            error : float
                The maximum error. 
            converged: bool
                The convergence state. 
            model_id : str
                The id of the model. 
            var_id : str
                The id of variable with hte highest error. 

        Raises
        ------
        `ComputeError` if something went wrong.

        """       
        
        try:
            convergence_iter = []
            for model_id in self.order:
                # Check only models containing ouput vectors
                if len(self.models[model_id].y) > 0:
                    # List holding the relative errors for the model
                    convergence_model = []
                    for var_id in self.models[model_id].get_y_vars():
                        # Get var values on the desired time frame
                        y_new = new_state[model_id].get_var(var_id, t_frame)
                        y_old = old_state[model_id].get_var(var_id, t_frame)
                        # Compute the 2-norm of the difference of y_new and y_old
                        delta = np.linalg.norm(np.array(y_new) - np.array(y_old), 2)
                        # Compute the max norm of y_old
                        norm = np.linalg.norm(y_old, np.inf)
                        # Compute the relative error 
                        # Divide delta and norm only if norm <> 0
                        error = delta / norm if norm else delta
                        # Convergence check  (error < epsilon)
                        converged = bool(error < self.epsilon)
                        # Append results to list
                        convergence_model.append([error, converged, model_id, var_id])
                    # Append the element with the maximum error
                    convergence_iter += [max(convergence_model)]

            # Return the convergence list
            return convergence_iter
        except:
            # Raise exception
            raise exception.ComputeError(self.models[model_id].name, model_id)
    
    def compute_model(self, model_id):
        """
        Computes a model. Raises a ComputeError if something went wrong.

        Parameters
        ----------
        model_id : str
            The id of the model to be computed. 

        Raises
        ------
        `ComputeError` if something went wrong.

        """

        try:
            # Get model from dictionary
            model = self.models[model_id]
            
            # Get compute args for the model
            kwargs = {} 
            if model_id in self.compute_kwargs:
                kwargs = self.compute_kwargs[model_id]

            # Perform computation
            if model.threadsafe:
                model.compute(
                    simulation_id=self.simulation_id, 
                    model_id=model_id, 
                    **kwargs)
            else:
                # Acquire lock
                with self.lock:
                    # Compute
                    model.compute(
                        simulation_id=self.simulation_id, 
                        model_id=model_id, 
                        **kwargs)

        except:
            # Raise exception
            raise exception.ComputeError(model.name, model_id)
      
    def compute_frame(self, t_frame):
        """
        Computes a waveform segment. Raises a ComputeError if
        something went wrong. Returns a list containing the
        convergence state, the number of frame iterations and 
        the convergence data for each iteration.

        Parameters
        ----------
        t_frame : list
            The time frame for the computation.

        Returns
        -------
        converged, frame_iter, convergence_frame: tupel
            A tupel containing the containing the convergence state, 
            the number of frame iterations and the convergence data 
            for each iteration.

            converged : bool
                The convergence stat of the frame.
            frame_iter : int
                The number of frame iterations.
            convergence_frame : list
                The rsults of the compute_convergence function for
                each iteration.

        See also
        --------
        compute_convergence : Computes the convergence between two iterations.

        """
                
        # List holding the convergence data for the frame
        convergence_frame = []
              
        # Store the last state
        old_state = self.frames[-1]
        for i in range(self.max_iter_frame):
            # Initialize the new state with the last state
            self.models = copy.deepcopy(self.frames[-1])

            if self.step_type == "gauss-seidel":
                # Compute the subsystems
                for model_id in self.order:
                    # Prepare model coupling
                    self.prepare_model_coupling(old_state, model_id, t_frame)
                    # Solve the model
                    self.compute_model(model_id)
            else:
                tasks = []
                 # Compute the subsystems
                for model_id in self.order:
                    # Prepare model coupling
                    self.prepare_model_coupling(old_state, model_id, t_frame)

                with ThreadPoolExecutor() as executor:
                    for model_id in self.order:
                        executor.submit(self.compute_model, model_id)
                                    
            # Compute convergence for every model and
            # all of its output variables
            convergence_iter = self.compute_convergence(
                self.models, 
                old_state, 
                t_frame
            )
            # Append the convergence result
            convergence_frame.append(convergence_iter)

            # Return if the simulation has converged
            if np.all(list(item[1] for item in convergence_iter)):
                # Return convergence state, number of frame iterations 
                # and convergence data
                return True, i + 1, convergence_frame

            # Backup current state for next iteration
            old_state = self.models
        
        # Max iteration depth was reached
        return False, self.max_iter_frame, convergence_frame
    
    def compute(
            self, t_start, t_end, t_out=None, frame_length=0, 
            min_frame_length=0, max_frame_length=0, max_iter_frame=0, 
            points_per_frame=101, max_iter=5000, iter_threshold=1, 
            alpha=1.5, beta=0.25, epsilon=0.001, step_type="gauss-seidel",
            verbose = True):
        """
        Computes the waveform relaxation. Raises a ComputeError if
        something went wrong. Calls the callbacks 
            on_simulation_started
            on_frame_finished
            on_simulation_finished
        if they are provided.

        Parameters
        ----------
        t_start : float
            Start time of the computation.
        t_end : float
            End time of the computation.
        t_out : list, optional
            The time frame for the result ouput. Default = None. 
        frame_length : float, optional
            The frame length of thte inital segment. Default = 0.
        min_frame_length : float, optional
            The minimum frame length. The segments can't get smaller
            than this value. Default = 0 (Automatically adjusted). 
        max_frame_length : float, optional
            The maximum frame length. The segments can't get larger
            than this value. Default = 0 (Automatically adjusted).
        max_iter_frame : int, optional
            The maximum number of iterations that are allowed.
            Default = 0 (Automatically adjusted). 
        points_per_frame : int, optional
            The number of points per segment.
            Default = 201. 
        max_iter : int, optional
            The maximum number of overall iterations.
            Default = 5000.
        iter_threshold : int, optional
            The iteration threshold. Used for segment adaption.
            Default = 1. 
        alpha : float, optional
            The expansion factor. A segment grows by this factor if the
            conditions are fullfilled.
            Default = 1.5. 
        beta : float, optional
            The contraction factor. A segment shrinks by this factor if the
            conditions are fullfilled.
            Default = 0.25.
        epsilon : float, optional
            The maximum allowed tolerance, used for the convergence test.
            Default = 0.0001.
        step_type : str, optional
            The waveform steptype. Must be one of 'gauss-seidel' or 'jacobi'.
            Default = 'gauss-seidel'.
        verbose : bool, optional
            If set to True, a bunch of state logs are printed on the console.
            Default = True.

        Raises
        ------
        `ParameterError` if parameters are inconsistent.

        """
        
        # Sanity checks
        if step_type != "gauss-seidel" and step_type != "jacobi":
            raise exception.ParameterError(
                "Parameter 'step_type' must be 'gauss-seidel' or 'jacobi'")
        if alpha < 1.0:
            raise exception.ParameterError(
                "Parameter 'alpha' must be greater or equal than 1.0")
        if beta >= 1.0:
            raise exception.ParameterError(
                "Parameter 'beta' must be less than 1.0")
        if t_end <= t_start:
            raise exception.ParameterError(
                "Parameter 't_end' must be greater than 't_start'")
            
        # Store current time
        timer_start = time.time()
        
        # Store job properties
        self.t_start = t_start
        self.t_end = t_end
        self.epsilon = epsilon
        self.frame_length = frame_length
        self.min_frame_length = min_frame_length
        self.max_frame_length = max_frame_length
        self.max_iter_frame = max_iter_frame
        self.points_per_frame = points_per_frame
        self.max_iter = max_iter
        self.iter_threshold = iter_threshold
        self.alpha = alpha
        self.beta = beta
        self.step_type = step_type
        
        # Set minimum length of frame
        if self.max_iter_frame <= 0:
            self.max_iter_frame = len(self.models) + 4
        # Adjust length of frames if frame_length was not set
        if self.frame_length > t_end - t_start or self.frame_length <= 0:
            self.frame_length = 0.02 * (t_end - t_start)
        # Set minimum length of frame
        if self.min_frame_length <= 0:
            self.min_frame_length = self.frame_length * self.beta**3
        # Set maximum length of frame
        if self.max_frame_length <= 0:
            self.max_frame_length = self.frame_length * self.alpha**3
        # Frame state variable
        frame_state = ""

        # Call user callback function if provided
        if self.on_simulation_started != None:
            self.on_simulation_started(self)

        # print job properties
        if verbose:
            msg = "Starting '{}'\n".format(self.simulation_id)
            msg += "    t_start = {:.3E}\n".format(self.t_start)
            msg += "    t_end = {:.3E}\n".format(self.t_end)
            msg += "    frame_length = {:.3E}\n".format(self.frame_length)
            msg += "    min_frame_length = {:.3E}\n".format(self.min_frame_length)
            msg += "    max_frame_length = {:.3E}\n".format(self.max_frame_length)
            msg += "    max_iter_frame = {:d}\n".format(self.max_iter_frame)
            msg += "    points_per_frame = {:d}\n".format(self.points_per_frame)
            msg += "    max_iter = {:d}\n".format(self.max_iter)
            msg += "    iter_threshold = {:d}\n".format(self.iter_threshold)
            msg += "    alpha = {:.3E}\n".format(self.alpha)
            msg += "    beta = {:.3E}\n".format(self.beta)
            msg += "    epsilon = {:.3E}\n".format(self.epsilon)
            msg += "    step_type = '{}'".format(self.step_type)
            print(msg)
            
        # Prepare the frames list holding the results for each frame
        if len(self.frames) > 0:
            self.models = copy.deepcopy(self.frames[0])
            self.num_iter_all = 0
            self.num_iter_used = 0
            self.num_converged_frames = 0
            self.num_restarted_frames = 0
            self.num_canceled_frames = 0
            self.duration = 0
            del self.frames[1:]
            del self.convergence[:]
            del self.statistics[:]
        else:
            self.frames = [copy.deepcopy(self.models)]

        # Set the start time for the frame
        t_frame_start = t_start
        t_frame_end = t_start + self.frame_length
        
        # Loop until we have reached t_end
        while t_frame_start < t_end and self.num_iter_all < self.max_iter:
            
            # Compute equidistant grid points for the time frame
            t_frame = np.linspace(
                t_frame_start, 
                min(t_frame_end, t_end), 
                self.points_per_frame)
            
            # Store current frame number
            num_frame = len(self.frames)

            # Store current time
            frame_timer_start = time.time()
            
            # Compute the frame
            converged, num_iter_frame, convergence_frame = \
                self.compute_frame(t_frame)
            
            # Compute duration
            frame_duration = time.time() - frame_timer_start
            
            # Increment num_iter_all
            self.num_iter_all += num_iter_frame

            # If we have reached convergence then store the results
            if converged:
                
                # Set frame state
                frame_state = "Finished"
                self.num_iter_used += num_iter_frame

                # Append results to the result lists
                self.frames.append(copy.deepcopy(self.models))
                self.convergence.append(convergence_frame)
                self.num_converged_frames += 1

                # Compute the limits of the next frame
                prev_frame_length = t_frame[-1] - t_frame[0]
                next_fame_length = prev_frame_length * self.alpha
                if num_iter_frame < self.max_iter_frame - self.iter_threshold:
                    t_frame_start = t_frame[-1]
                    t_frame_end = t_frame[-1] + min(
                        next_fame_length, self.max_frame_length)
                    
                else:
                    t_frame_start = t_frame[-1]
                    t_frame_end = t_frame[-1] + prev_frame_length

            else:
                # Shrink the time frame (convergence not reached yet)
                prev_frame_length = t_frame[-1] - t_frame[0]
                next_frame_length = prev_frame_length * self.beta

                # Cancel and proceed if we can not shrink the limits further
                if next_frame_length < self.min_frame_length:
                    # Set frame state
                    frame_state = "Canceled"

                    # Append results to the result lists
                    self.frames.append(copy.deepcopy(self.models))
                    self.convergence.append(convergence_frame)
                    self.num_canceled_frames += 1

                    # Set the limits for the next frame
                    t_frame_start = t_frame[-1]
                    t_frame_end = t_frame[-1] + self.min_frame_length
                else:
                    # Set frame state
                    frame_state = "Restarted"
                    # Restart the frame with the shrinked limits
                    t_frame_end = t_frame[0] + next_frame_length
                    self.num_restarted_frames += 1

            # Get the max error for logging purposes
            max_error = max(convergence_frame[-1])
            
            # Append to statistics list
            self.statistics.append(
                [time.time() - timer_start, num_frame, frame_state, 
                 t_frame[0], t_frame[-1],frame_duration, num_iter_frame,
                 max_error[0], max_error[1],  max_error[2],  max_error[3]])
            
            # Print frame statistics
            if verbose:
                msg = ("{} frame #{:d} from {:.3E}s to {:.3E}s in "
                       "{:.3E}s afer {:d} iterations (Error: {:.3E} "
                       "| Convergence: {} | {}.{}).").format(
                        frame_state, num_frame, t_frame[0], t_frame[-1], 
                        frame_duration, num_iter_frame, max_error[0], 
                        max_error[1], max_error[2], max_error[3])
                print(msg)
            
            # Call user callback function if provided
            if self.on_frame_finished != None:
                self.on_frame_finished(self)
            
 
        # Aggregate the result in the model dictionary
        self.prepare_result(t_out)
        
        # Compute duration
        self.duration = time.time()-timer_start

        # Log current state
        if verbose:
            msg = ("Finished waveform in {:.3E}s after {:d} iterations "
                   "({:d} overall), {:d} frames converged, {:d} "
                   "frames canceled, {:d} frames restarted.").format(
                    self.duration, self.num_iter_used, self.num_iter_all, 
                    self.num_converged_frames, self.num_canceled_frames, 
                    self.num_restarted_frames)
            print(msg)
            
        # Call user callback function if provided
        if self.on_simulation_finished != None:
            self.on_simulation_finished(self)