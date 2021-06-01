

######################################
def g_r(strc,dr=0.1,cutoff_r=10.):
    """
    Function that computes radial distribution function
    between 0. and cutoff_r with the grid on the distance 
    axis defined by dr.
    Returns a dictionary with keys labeling the types of atoms 
    for which g(r) is calculated (e.g. 'Si-Si','Si-O', etc.)
    and the values are corresponding g(r)
    """

    from copy import deepcopy
    import numpy as np
    from pylada.crystal import neighbors
    import itertools 

    # rescale the structure
    cell=deepcopy(strc.cell)
    scale=deepcopy(strc.scale)
    positions=deepcopy([atom.pos for atom in strc])

    strc.scale=1.
    strc.cell=cell*float(scale)
    for ii in range(len(strc)):
        strc[ii].pos=np.array(positions[ii])*float(scale)
    # DONE

    # number density
    n_dense = len(strc)/float(strc.volume)

    # the distance axis used to calculate rdf
    rs = np.arange(0.,cutoff_r+dr,dr)

    atom_types=list(set([atom.type for atom in strc]))
    atom_types_indices={at:[ii for ii in range(len(strc)) if strc[ii].type==at] for at in atom_types}

    g_r_dict={}


    for type1,type2 in itertools.product(atom_types,atom_types):

        n_dense_type2 = len(atom_types_indices[type2])/float(strc.volume)

        # dummy g_r
        gr = np.zeros(len(rs))

        for atom_index in atom_types_indices[type1]:

            # get the neighbors
            n_nghs = 1000
            nghs = neighbors(strc,n_nghs,strc[atom_index].pos,0.3)

            # make sure that neighbors are further away than cutoff_r
            while nghs[-1][-1]<cutoff_r:
                n_nghs = n_nghs+5
                nghs = neighbors(strc,n_nghs,strc[atom_index].pos,0.3)

            nghs = [ngh for ngh in nghs if ngh[0].type==type2]

            # count neighbors into bins between r and r+dr
            no_nghs = [ len([ ng for ng in nghs if r-0.5*dr <= ng[-1] < r+0.5*dr ]) / (4*np.pi*r**2*dr)  for r in rs[1:]]
            no_nghs.insert(0,0.)

            gr = gr + np.array(no_nghs)

#        gr = gr/n_dense_type2/len(atom_types_indices[type1])
        gr = gr/n_dense/len(atom_types_indices[type1])

        g_r_dict[type1+'-'+type2]=np.array(list(zip(rs,gr)))

    return g_r_dict



######################################
def n_r(strc,dr=0.1,cutoff_r=10.):
    """
    Function that computes number of atoms at a distance r 
    between 0. and cutoff_r with the grid on the distance 
    axis defined by dr
    """

    from copy import deepcopy
    import numpy as np
    from pylada.crystal import neighbors

    # rescale the structure
    cell=deepcopy(strc.cell)
    scale=deepcopy(strc.scale)
    positions=deepcopy([atom.pos for atom in strc])

    strc.scale=1.
    strc.cell=cell*float(scale)
    for ii in range(len(strc)):
        strc[ii].pos=np.array(positions[ii])*float(scale)
    # DONE

    # the distance axis used to calculate rdf
    rs = np.arange(0.,cutoff_r+dr,dr)

    # dummy g_r
    nr = np.zeros(len(rs))

    for atom in strc:

        # get the neighbors
        n_nghs = 100
        nghs = neighbors(strc,n_nghs,atom.pos,0.3)

        # make sure that neighbors are further away than cutoff_r
        while nghs[-1][-1]<cutoff_r:
            n_nghs = n_nghs+5
            nghs = neighbors(strc,n_nghs,atom.pos,0.3)

        # count neighbors into bins between r and r+dr
        no_nghs = [ len([ ng for ng in nghs if ng[-1] < r+0.5*dr ])  for r in rs[1:]]
        no_nghs.insert(0,0.)

        nr = nr + np.array(no_nghs)

    nr = nr/len(strc)

    return zip(rs,nr)

