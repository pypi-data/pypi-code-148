from check_prime import query_maker

my_query = query_maker.apply_rule('employee_id', 'AS345', 'employee')

print(my_query)
