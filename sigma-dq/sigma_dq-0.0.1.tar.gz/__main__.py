from sigma_dq.sigma_dq_check_ends_with import sigma_dq_check_ends_with


target_table = 'edap_transform.Purchase_order'
my_query = sigma_dq_check_ends_with('JDE_UDC_PURCHASE_DOCUMENT_TYPE_DESC','DT',target_table,
'Incremental',meta={'dq_master_id' : 1})

print(my_query)
