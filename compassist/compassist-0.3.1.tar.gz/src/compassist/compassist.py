# imports
import numpy as np
import math
import matplotlib.pyplot as plt
import itertools


def shiny_hunt(
    gen,
    masuda=False,
    shiny_charm=False,
    encounter_rate=100,
    attempt_time=15,
    hatch_time=None,
    verbose=False,
):
    """Calculates and prints number of attempts (and expected time) required to find a shiny pokemon

    Parameters
    ----------
    gen : int
        integer denoting generation of pokemon
    masuda : bool, optional
        is the player using masuda method
    shiny_charm : bool, optional
        does the player have a shiny charm
    encounter_rate : int or float
        rate of encounter of the pokemon (only for wild encounters)
    attempt_time : int, optional
        time (in seconds) representing average time taken to encounter a pokemon, or soft reset
    hatch_time : int, optional
        time (in seconds) to hatch a single pokemon egg
    verbose : bool, optional
        Controls format of returned probability. Default (True) prints results as statements, False returns a dict.

    Returns
    -------
    dict
        dictionary containing probabilities as keys and number of attempts/hrs values as tuples

    Examples
    --------
    >>> shiny_hunt(gen=7, encounter_rate=25, attempt_time=15, shiny_charm=True, verbose=True)
    There is a 25% chance to get a shiny encounter in 3144 encounters
    This would take an approximate of 13.1 hours.
    ================================
    There is a 50% chance to get a shiny encounter in 7568 encounters
    This would take an approximate of 31.53 hours.
    ================================
    There is a 75% chance to get a shiny encounter in 15136 encounters
    This would take an approximate of 63.07 hours.
    ================================
    There is a 90% chance to get a shiny encounter in 25144 encounters
    This would take an approximate of 104.77 hours.
    ================================
    There is a 99% chance to get a shiny encounter in 50280 encounters
    This would take an approximate of 209.5 hours.
    ================================

    output of shiny_hunt() when verbose is set to true

    >>> shiny_hunt(gen=7, encounter_rate=35, attempt_time=15, shiny_charm=True, verbose=False)
    {'25%': (1965, 8.19), '50%': (4730, 19.71), '75%': (9460, 39.42), '90%': (15715, 65.48), '99%': (31425, 130.94)}

    output of shin_hunt() when verbose is set to false

    """

    # make sure all inputs are legal
    if not isinstance(gen, int):
        raise TypeError("Gen must be an integer")
    if gen < 1 or gen > 9:
        raise ValueError("Gen must be in the range [1-9]")
    if not isinstance(encounter_rate, float):
        if not isinstance(encounter_rate, int):
            raise TypeError("Encounter rate must be a number")
    if encounter_rate <= 0 or encounter_rate > 100.0:
        raise ValueError("Encounter rate must be in the range [0-100]")
    if not isinstance(attempt_time, int):
        raise TypeError("Attempt time must be an integer (in seconds)")
    if attempt_time < 0:
        raise ValueError("Attempt time must be positive")
    if not isinstance(shiny_charm, bool):
        raise TypeError("Shiny charm must be a boolean")
    if shiny_charm and gen < 5:
        raise Exception("Shiny charm did not exist prior to gen 5")
    if masuda and gen < 4:
        raise Exception("Masuda method did not exist prior to gen 4")

    # base rate of encountering a shiny pokemon before gen 6
    base_rate = 1 / 8192

    # base rate doubles in gen 6 and above
    if gen > 5:
        base_rate *= 2

    prob = base_rate

    # probability increases if player has shiny charm equipped
    if shiny_charm:
        prob += 2 * base_rate

    # probability increases further when using masuda method
    if masuda:
        prob += 4 * base_rate
        if gen > 4:
            prob += base_rate

    expected_values = [0.25, 0.5, 0.75, 0.9, 0.99]
    results = {}

    for value in expected_values:
        # calculate number of attempts
        n = int(np.round(np.log(1 - value) / np.log(1 - prob), 0))
        if masuda:
            if hatch_time:
                results[f"{int(value * 100)}%"] = (
                    n,
                    np.round(n * hatch_time / 3600, 2),
                )
            else:
                results[f"{int(value * 100)}%"] = n
        elif encounter_rate < 100:
            avg_attempts = int(
                np.round(np.log(1 - 0.9) / np.log(1 - (encounter_rate / 100)), 0)
            )
            results[f"{int(value * 100)}%"] = (
                n * avg_attempts,
                np.round(n * avg_attempts * attempt_time / 3600, 2),
            )
        else:
            results[f"{int(value * 100)}%"] = (n, np.round(n * attempt_time / 3600, 2))

    # print the output to console if verbose is set to true
    if verbose:
        for key in results:
            if masuda:
                if hatch_time:
                    print(
                        f"There is a {key} chance to hatch a shiny in {results[key][0]} attempts"
                    )
                    print(f"This would take an approximate of {results[key][1]} hours.")
                else:
                    print(
                        f"There is a {key} chance to hatch a shiny in {results[key]} attempts"
                    )
            else:
                print(
                    f"There is a {key} chance to get a shiny encounter in {results[key][0]} encounters"
                )
                print(f"This would take an approximate of {results[key][1]} hours.")
            print("================================")

    # return dictionary otherwise
    else:
        return results


def boss_completion(rates, base_rate=None, attempts=None, verbose=True):
    """Calculates expected wins/finishes required to obtain/complete a specific set of tasks
         i.e. obtaining all unique drops from a boss

     Parameters
     ----------
     rates : list
         a list of probabilities as floats between 1 and 0. When base_rate is defined must sum to 1

     base_rate : float
         a probability between 1 and 0. In the case where there is a fixed rate of recieving an item table roll

     attempts : numeric
         number of attempts. Rounds to nearest int, rounds negatives to 0. Enables function to return probability of
         completion for number of attempts

     verbose : bool
         enables printed output

     Returns
     -------
    float
         should always converge to 1.0 on success

    int
         expected number of attempts required to achieve goal

     float
         percentage between 0 and 100. Only returned when argument 'attempts' is not None

     Examples
     ---------
     >>> boss_completion(rates = [7/24, 7/24, 3/24, 2/24, 2/24, 2/24, 1/24], base_rate= 1/20, attempts = 673, verbose= False)
     (1.0, 673, 63.24)

     >>> boss_completion(rates = [7/24, 7/24, 3/24, 2/24, 2/24, 2/24, 1/24], base_rate= 1/20, attempts = 673, verbose= True)
     Expected Completion: 673
     Probability of Completion at 673 Attempts: 63.24%
     (1.0, 673, 63.24)
    """

    # Check that rates add to one for a base rate
    if round(sum(rates), 3) != 1.0 and base_rate is not None:
        print("Rates do not add to 1 even though a base rate is provided")
        return None

    # Check no rate is >1 or negative
    for rate in rates:
        if rate > 1 or rate < 0:
            print("Rates cannot be greater than 1 or less than 0")
            return None

    # generate permutations (list of lists)
    permutations = list(itertools.permutations(rates))

    # initializing overall counters
    total_count = 0
    total_probability = 0

    # iterate through permutations
    for perm in permutations:

        # initializing permutation counters
        permutation_count = 0
        remaining_prob = 1
        permutation_prob = 1

        # expected attempts for next permutation event, base rate
        if base_rate is not None:
            for item in perm:
                permutation_count += 1 / remaining_prob * 1 / base_rate
                remaining_prob -= item

        # expected attempts for next permutation event, no base rate
        else:
            for item in perm:
                permutation_count += 1 / remaining_prob
                remaining_prob -= item

        # probability of the permutation sequence
        for i in range(len(perm)):
            j = i - 1
            total = 1
            while j > -1:
                total -= perm[j]
                j -= 1
            permutation_prob = permutation_prob * perm[i] / total

        # count up total probabilities and total count
        total_probability += permutation_prob
        total_count += permutation_count * permutation_prob

    if round(total_probability, 3) != 1.0:
        raise ValueError(
            "Total Probability did not converge to 1.0. Something went wrong"
        )

    if verbose == True:
        print(f"Expected Completion: {int(total_count)}")

    # Approximate probability as a single event for binomial probability
    if attempts is not None:

        attempts = int(attempts)
        if attempts < 0:
            attempts = 0

        # edge case, 0% for less attempts than total items
        if attempts < len(rates):
            if verbose == True:
                print(f"Probability of Completion at {attempts} Attempts: 0%")
            p1_percent = 0
            return round(total_probability, 3), int(total_count), round(p1_percent, 2)

        else:
            # calculate prob not done
            x = 0
            n_choose_x = math.factorial(attempts) / (
                math.factorial(x) * math.factorial((attempts - x))
            )
            p0 = (
                n_choose_x
                * (1 / total_count**x)
                * ((1 - 1 / total_count) ** (attempts - x))
            )

            # calculate prob done (1 - not done)
            p1 = 1 - p0
            p1_percent = p1 * 100

            if verbose == True:
                print(
                    f"Probability of Completion at {attempts} Attempts: {round(p1_percent,2)}%"
                )

            return round(total_probability, 3), int(total_count), round(p1_percent, 2)

    return round(total_probability, 3), int(total_count)


# dry_calc function
def dry_calc(p, n, verbose=True, plot=True):
    """Calculates probability of at least one occurrence of an event given the number of attempts.

    Parameters
    ----------
    p : float
        Probability of event occurrence; a decimal between 0 and 1.
        
    n : int
        The number of attempts; a whole number greater than or equal to 0.
        
    verbose : bool, Optional
        Controls format of returned probability;
        Default (True) returns result printed in a statement; 
        False returns numerical probability as a float.
        
    plot : bool, Optional
        Controls printing of plot showing where the resulting probability lies on the binomial distribution; 
        Default is True.
    
    Returns
    -------
    str 
        String statement containing the probability of at least one occurrence of event given the number of trials as a percentage (default).

    float
        Probability of at least one occurrence of event given the number of trials as a decimal (if verbose set to False).

    Examples
    --------
    >>> dry_calc(0.2, 5, verbose=False, plot=False)
    0.6723199999999999

    >>> dry_calc(0.2, 5, verbose=True, plot=False)
    'There is a 67.2% chance of the event occurring at least once after you play 5 attempts.'
    """
    # check probability input is a float between 0 and 1
    if not (0 <= p <= 1):
        raise ValueError("Probability, p, should be a decimal between 0 and 1!")

    # check n input is a positive integer
    if not isinstance(n, int) or not (n >= 0):
        raise ValueError(
            "Number of attempts, n, should be an integer greater than or equal to 0!"
        )

    # calculate p(0): binomial probability of the event occurring 0 times given n trials and probability p
    x = 0
    n_choose_x = math.factorial(n) / (math.factorial(x) * math.factorial((n - x)))
    p0 = n_choose_x * (p**x) * ((1 - p) ** (n - x))

    # calculate probability of at least 1 occurrence: 1 - p(0)
    p1 = 1 - p0
    p1_percent = p1 * 100

    # show plot if requested
    if plot:
        pn = 0
        pp = dry_calc(p, pn, verbose=False, plot=False)

        # initiate x and y lists
        px = [pn]
        py = [pp]

        while pp <= 0.99:
            pn += 1
            pp = dry_calc(p, pn, verbose=False, plot=False)
            px.append(pn)
            py.append(pp)

        plt.bar(px, py)
        plt.plot(n, p1, marker="X", ms=15, mfc="red", label=round(p1, 3))
        plt.xlabel("Number of attempts")
        plt.ylabel("Probability")
        plt.legend()
        plt.show()

    # check verbose argument to return correct output
    if verbose:
        result = f"There is a {p1_percent:.1f}% chance of the event occurring at least once after you play {n} attempts."
        return result

    else:
        return p1


def pts_calc(points_attempt, time_attempt, target_points, verbose=True):
    """Calculates and returns the list of time required (in ranked order) to achieve target points using the different options provided in input 

    Parameters
    ----------
    points_attempt : list of float or int
        number of points obtained in each attempt
    time_attempt : list of float or int
        time taken (in minutes) for each attempt
    target_point :  float or int
        number of points targetted to reach
    verbose : bool, optional
        Controls format of returned time taken. Default (True) prints results as statements, False returns a list.

    Returns
    -------
    time : list of float
        time required (in ranked order of minutes) to achieve target points using the different options provided in input 

    Examples
    --------
    output of pts_calc() when verbose is set to True default
    >>> pts_calc([100,20,120,150,200,30], [2,3,2,5,6,2], 200.0)
    Rank 1 using the strategy 120 points per 2 minutes you can reach your target in 3.3333333333333335 minutes
    Rank 2 using the strategy 100 points per 2 minutes you can reach your target in 4.0 minutes
    Rank 3 using the strategy 200 points per 6 minutes you can reach your target in 6.0 minutes
    Rank 4 using the strategy 150 points per 5 minutes you can reach your target in 6.666666666666667 minutes
    Rank 5 using the strategy 30 points per 2 minutes you can reach your target in 13.333333333333334 minutes
    Rank 6 using the strategy 20 points per 3 minutes you can reach your target in 30.0 minutes
    
    output of pts_calc() when verbose is set to False
    >>> pts_calc([100,20,120,150,200,30], [2,3,2,5,6,2], 200.0,  verbose=False)
    pts_calc([100,20,120,150,200,30], [2,3,2,5,6,2], 200.0,  verbose=False)
    
    """
    
    
    # checking data types and value 
    if not isinstance(target_points, (int, float)):
        raise TypeError("target points must be of type float or int")
    if not isinstance(points_attempt, list):
        raise TypeError("points_attempt must be of type list of float or int")
    if not isinstance(time_attempt, list):
        raise TypeError("time_attempt must be of type list of float or int")
    if len(points_attempt) != len(time_attempt):
        raise TypeError("The length of points attempt and time taken do not match")
    for x in points_attempt:
        if x < 1:
            raise TypeError("points achieved cannot be negative or zero")
    for x in time_attempt:
        if x < 1:
            raise TypeError("time taken cannot be negative or zero")
            
            
    
    scoring_rate = []
    # calculating the scoring rate as per the different options from input    
    for i in range(0, len(points_attempt)):
        scoring_rate.append(float(points_attempt[i]/time_attempt[i]))
    
    time_required = []
    # calculating the time required to reach the threshold points using the scoring rate
    for x in range(0, len(scoring_rate)):
        time_required.append(float(target_points/ scoring_rate[x]))
        
        
        
    # sorting the best time and strategy based on options available and target
    indices_of_best_strat = np.argsort(time_required)
    
    
    ranking = 1
    sorted_time_required = []
    
    # print the output to console if verbose is set to true
    if verbose:
        for x in indices_of_best_strat:
            print(
                f"Rank {ranking} using the strategy {points_attempt[x]} points per {time_attempt[x]} minutes you can reach your target in {time_required[x]} minutes"
            )
            ranking += 1
    else:
        for x in indices_of_best_strat:
            sorted_time_required.append(time_required[x])
        return sorted_time_required
