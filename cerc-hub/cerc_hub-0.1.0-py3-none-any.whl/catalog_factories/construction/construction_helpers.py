from helpers import constants as cte

nrel_to_function = {
  'residential': cte.RESIDENTIAL,
  'midrise apartment': cte.MID_RISE_APARTMENT,
  'high-rise apartment': cte.HIGH_RISE_APARTMENT,
  'small office': cte.SMALL_OFFICE,
  'medium office': cte.MEDIUM_OFFICE,
  'large office': cte.LARGE_OFFICE,
  'primary school': cte.PRIMARY_SCHOOL,
  'secondary school': cte.SECONDARY_SCHOOL,
  'stand-alone retail': cte.STAND_ALONE_RETAIL,
  'hospital': cte.HOSPITAL,
  'outpatient healthcare': cte.OUT_PATIENT_HEALTH_CARE,
  'strip mall': cte.STRIP_MALL,
  'supermarket': cte.SUPERMARKET,
  'warehouse': cte.WAREHOUSE,
  'quick service restaurant': cte.QUICK_SERVICE_RESTAURANT,
  'full service restaurant': cte.FULL_SERVICE_RESTAURANT,
  'small hotel': cte.SMALL_HOTEL,
  'large hotel': cte.LARGE_HOTEL,
  'industry': cte.INDUSTRY
}

nrcan_to_function = {
  'residential': cte.RESIDENTIAL,
}

reference_standard_to_construction_period = {
  'non_standard_dompark': '1900 - 2004',
  'ASHRAE 90.1_2004': '2004 - 2009',
  'ASHRAE 189.1_2009': '2009 - PRESENT'
}

nrel_surfaces_types_to_hub_types = {
  'exterior wall': cte.WALL,
  'interior wall': cte.INTERIOR_WALL,
  'ground wall': cte.GROUND_WALL,
  'exterior slab': cte.GROUND,
  'attic floor': cte.ATTIC_FLOOR,
  'interior slab': cte.INTERIOR_SLAB,
  'roof': cte.ROOF
}