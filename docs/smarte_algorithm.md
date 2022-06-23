# SMARTE ALGORITHM

# Inputs
* SBML model
* Observational data
* Ranges for parameters to estimate
* Parameters to estimate

# Outputs
* Parameter estimates


# Steps

    // Initializations
    parameter_values =  mid-point of range for each parameter to estimate
    kinetics_expressions = kinetics laws
    subset kinetics_expressions to those that include
      a floating species or flux for which data have been provided
      
    // Initial expectation
    simulated_values = simulation using midpoint of parameter ranges
      
    // Optimization
    done = False
    while not done:
	    initial_parameter_values = []
	    for expression in kinetics_expressions:
	        local_parameters = parameters in expression
	        data = applicable observational data
	          and simulation data in expression
	        local_parameter_estimates = fit local_parameters to data
	        initial_parameter_values.append(local_parameter_estimates)
	    parameter_estimates = global optimization(initial_parameter_values,
	      observational_data, max_number_iterations)
	      
	    // Expectation
	    simulated_values = simulations using parameter_estimates
	   
	    // Termination test
	    residuals = observed_values - simulated_values
	    if residuals are sufficiently small or unchanging
	        done = True
	        
	  // Return
	  return parameter_estimates
