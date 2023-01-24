
class Datatable_JS :

    def __init__(self,params= None):
        self.paging                  = params["paging"] if  'paging' in  params else 'true'
        self.scrollY                 = params["scrollY"] if  'scrollY' in  params else '60vh'
        self.ordering                = params['ordering']
        self.ajax_token              = params['ajax_token']
        self.dt_column_options       = params['dt_column_options']
        self.dt_drawCallback_options = params['dt_drawCallback_options']
        self.dt_columnDefs_options   = params['dt_columnDefs_options']
        self.url_ajax                = params["url_ajax"]
        self.ajax_option             = params["ajax_option"]
        self.page_length             = params["page_length"] if  params["page_length"] else 25
        self.script                  = params["script"] if  params["script"] else ""
        self.order                   = params["order"] if  params["order"] else '[ 0, "asc" ]'
        self.affiche_script_balise   = params["affiche_script_balise"] if  params["affiche_script_balise"] else 0
        self.responsive              = params["responsive"] if  params["responsive"] else True
        self.titre                   = params['titre'] if  params['titre'] else ''
        self.bouton                  = params['bouton_controle'] if params['bouton_controle'] else ""
        self.fixed_column            = params['fixed_columns'] if params['fixed_columns'] else ""
        self.btn_pdf_copy            = "" if params['btn_pdf_copy'] else """{
																					extend: "pdf",
																					title: '"""+self.titre+"""',
																					text: "<span class="fa fa-file-pdf-o"></span> PDF",
																					exportOptions: {
																						/*columns: ":visible"*/
																						columns: "thead th:not(.noExport)",
																						orientation: "landscape",
																						pageSize: "LEGAL"
																					}
																				},"""
    

    def set_options(self,arr_option):
        dt_options = ""
        for key_option in arr_option:
            dt_options += "{}: {}, \n".format(key_option,arr_option[key_option])
        return dt_options
    

    def set_ajax_options(self,arr_data = None):
        ajax_options = ""
        for key_ajax in arr_data:
            ajax_options += "data.{} = {} \n".format(key_ajax,arr_data[key_ajax])
        return ajax_options
    

    def jquery(self,id):
        dt_options_columns = self.set_options(self.dt_column_options)
        dt_callback        = self.set_options(self.dt_drawCallback_options)
        dt_columnDefs      = self.set_options(self.dt_columnDefs_options)
        ajax_options       = self.ajax_option#self.set_ajax_options(self.ajax_option)
        
        output = ''
        output += """
        $('#"""+id+"""').DataTable().destroy();
        var dataTable"""+id+"""; 
                            dataTable"""+id+""" = $('#"""+id+"""').DataTable({
                                processing:true,
                                serverSide: true,
                                responsive: """+self.responsive+""",
                                order: ["""+self.order+"""],
                                """+dt_options_columns+"""
                                ajax:  {
                                    headers: {
                                        'Authorization': 'Bearer """+self.ajax_token+"""'
                                    },
                                    url : '"""+self.url_ajax+"""',
                                    type: "POST",
                                    data:"""+str(ajax_options)+""",
                                },
                                
                                ordering: """+self.ordering+""",
                                autoWidth: false,
                                scrollCollapse: true,
                                paging: """+self.paging+""",
                                scrollY: '"""+self.scrollY+"""' ,
                                retrieve: true,
                                """+dt_callback+dt_columnDefs+"""
                                select: "multi",
                                /*language: {
                                    processing:     "Traitement en cours...",
                                    search:         "Rechercher&nbsp:",
                                    lengthMenu:    "Afficher _MENU_ &eacutel&eacutements",
                                    info:           "Affichage de l\'&eacutel&eacutement _START_ &agrave _END_ sur _TOTAL_ &eacutel&eacutements",
                                    infoEmpty:      "Affichage de l\'&eacutelement 0 &agrave 0 sur 0 &eacutel&eacutements",
                                    infoFiltered:   "(filtr&eacute de _MAX_ &eacutel&eacutements au total)",
                                    infoPostFix:    "",
                                    loadingRecords: "Chargement en cours...",
                                    zeroRecords:    "Aucun &eacutel&eacutement &agrave afficher",
                                    emptyTable:     "Aucune donnée disponible dans le tableau",
                                    paginate: {
                                        first:      "Premier",
                                        previous:   "Pr&eacutec&eacutedent",
                                        next:       "Suivant",
                                        last:       "Dernier"
                                    },
                                    aria: {
                                        sortAscending:  ": activer pour trier la colonne par ordre croissant",
                                        sortDescending: ": activer pour trier la colonne par ordre décroissant"
                                    }
                                },*/
                                lengthMenu: [[5, 10, 15, 20, 25, 50,100, -1], [5, 10, 15, 20, 25, 50,100, 'All']],
                                pageLength: """+str(self.page_length)+""",
                                """+self.fixed_column+"""
                                dom: \'<"toolbar">lBfrtip\',
                                buttons: [
                                    """+self.bouton+"""
                                    {
                                        extend: "excel",
                                        title: '"""+self.titre+"""',
                                        text: '<span class="fa fa-file-excel-o"></span> Excel',
                                        exportOptions: {
                                            /*columns: ":visible",*/
                                            columns: "thead th:not(.noExport)"
                                        }
									},
                                    {
                                        extend: "copy",
                                        title: '"""+self.titre+"""',
                                        text: '<span class="fa fa-files-o"></span> Copy',
                                        exportOptions: {
                                            /*columns: ":visible"*/
                                            columns: "thead th:not(.noExport)"
                                        }
                                    },
									"""+self.btn_pdf_copy+"""
                                ]
                            }).columns.adjust().draw();
                            $(".dt-buttons").css("float","right");
                            $("div.toolbar").css("float","right");
                            """+self.script+"""
                        """
        return output
