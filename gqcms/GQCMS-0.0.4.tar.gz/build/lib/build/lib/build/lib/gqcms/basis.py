from gqcms import Determinant


def seniorityBasis(seniority_number, sites, nalpha, nbeta):
    """
    Create a basis of the seniority number
    """
    
    if seniority_number == 0 and (nalpha+nbeta)%2 == 1:
        raise ValueError("seniority number zero not possible with odd number of electrons")
    
    ref_det = Determinant(nalpha=nalpha, nbeta=nbeta, sites=sites)
    basis = [ref_det]
    
    # Seniority zero
    if seniority_number == 0:
        
        start_sites = ref_det.alpha_occ
        end_sites = [site for site in range(sites) if site not in ref_det.alpha_occ]
        
        # n is the number of pairs to excite, the maximum number of pairs that
        # can be excited is limited by the list who has the smallest number of sites.
        for n in range(1, min(len(start_sites), len(end_sites))+1):
            # Loop over every start site
            for i in range(0, len(start_sites)):
                # Loop over every end site
                for j in range(0, len(end_sites)):
                    
                    # Create the excitation lists
                    current_start_sites = start_sites[i:i+n]
                    current_end_sites = end_sites[j:j+n]
                    
                    # Check if the current excitation lists both has length n, continue if not
                    if len(current_start_sites) != n or len(current_end_sites) != n:
                        continue
                        
                    # Perform the excitations
                    det_copy = ref_det.copy()
                    
                    # Destroy alpha and beta electrons in start_sites
                    for start_site in current_start_sites:
                        det_copy.remove_alpha_orbital(start_site)
                        det_copy.remove_beta_orbital(start_site)

                    # Create alpha and beta electrons in end_site
                    for end_site in current_end_sites:
                        det_copy.add_alpha_orbital(end_site)
                        det_copy.add_beta_orbital(end_site)
                        
                    # Add det_copy to basis dict
                    basis.append(det_copy)
                    
    else:
        raise NotImplementedError("Only seniority zero basis is implemented currently.")
    
    return basis