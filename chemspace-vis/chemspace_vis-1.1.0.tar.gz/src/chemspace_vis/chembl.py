from chemspace_vis.utils import get_hac_from_smiles


def read_csv_activity(fn, activity='Emax', sep=';', relevant_tags=None):
    with open(fn) as f:
        lines = f.readlines()
    if relevant_tags is None:
        relevant_tags = {'Standard Type': -1,
                         'Standard Value': -1,
                         'Molecule ChEMBL ID': -1,
                         'Smiles': -1,
                         'Molecular Weight': -1,
                         'Assay Description': -1,
                         'Assay Type': -1,
                         'Assay ChEMBL ID': -1,
                         'Document ChEMBL ID': -1
                         }
    tags = [x[1:-1] for x in lines[0].strip().split(sep)]
    for i, tag in enumerate(tags):
        if tag in relevant_tags:
            assert relevant_tags[tag] == -1
            relevant_tags[tag] = i
    return ChemblActivity(lines[1:], activity, sep, relevant_tags)


class ChemblActivity:

    def __init__(self, lines, activity, sep, relevant_tags):
        self.activity = activity
        self.sep = sep
        if 'Molecule ChEMBL ID' not in relevant_tags:
            raise ValueError("For now, 'Molecule ChEMBL ID' must be in relevant_tags since it is the common identifier")
        self.tags = relevant_tags
        self.id_index = self.tags['Molecule ChEMBL ID']
        self.data_dict = dict()
        self.index_dict = dict()
        self.missing_data_ids = set()
        for tag in self.tags:
            self.data_dict[tag] = []
        self.contains_duplicates = False
        self.fill_dicts(lines)

    def fill_dicts(self, lines):
        i = 0
        for line in lines:
            ll = line.split(self.sep)
            for j in range(len(ll)):
                if ll[j].startswith('"'):
                    ll[j] = ll[j][1:-1]
            mol_id = ll[self.id_index]
            try:
                value = float(ll[self.tags['Standard Value']])
            except ValueError:
                self.missing_data_ids.add(ll[self.tags['Molecule ChEMBL ID']])
                continue
            if mol_id not in self.index_dict:
                self.index_dict[mol_id] = [i]
            else:
                self.index_dict[mol_id].append(i)
                self.contains_duplicates = True
            i += 1
            for tag in self.tags:
                if tag == 'Molecular Weight' or tag == 'Standard Value':
                    try:
                        self.data_dict[tag].append(float(ll[self.tags[tag]]))
                    except ValueError as e:
                        print(tag)
                        print(line)
                        raise e
                else:
                    self.data_dict[tag].append(ll[self.tags[tag]])
                if tag == 'Standard Type':
                    if self.activity is not None and ll[self.tags[tag]] != self.activity:
                        raise ValueError("Activity should be {}, but line {} is {}".format(self.activity, i,
                                                                                           ll[self.tags[tag]]))

    def print_duplicates(self):
        for mol_id in self.index_dict:
            if len(self.index_dict[mol_id]) >= 2:
                print(mol_id)
                for index in self.index_dict[mol_id]:
                    print(self.data_dict['Standard Value'][index], self.data_dict['Assay Description'][index])

    def generate_smiles_id_file(self, filename, mw_thresh=500, hac_thresh=None):
        with open(filename, "w") as f:
            for mol_id in self.index_dict:
                if self.data_dict['Molecular Weight'][self.index_dict[mol_id][0]] > mw_thresh:
                    continue
                if hac_thresh is not None:
                    if get_hac_from_smiles(self.data_dict['Smiles'][self.index_dict[mol_id][0]]) > hac_thresh:
                        continue
                f.write("{} {}\n".format(self.data_dict['Smiles'][self.index_dict[mol_id][0]], mol_id))

    def get_n_unique(self):
        return len(self.index_dict)

    def generate_id_activity_df(self, filename, use_mean=False, assay_filter=None, hac_filter=None):
        if assay_filter is not None:
            assert isinstance(assay_filter, list)
        with open(filename, "w") as f:
            if use_mean:
                f.write("mol_id activity\n")
            else:
                f.write("mol_id activity replicate\n")
            for mol_id in self.index_dict:
                value = 0
                count = 0
                for i, index in enumerate(self.index_dict[mol_id]):
                    if assay_filter is not None:
                        passed_filter = True
                        for af in assay_filter:
                            if af not in self.data_dict['Assay Description'][index]:
                                passed_filter = False
                        if not passed_filter:
                            continue
                    if hac_filter is not None:
                        if get_hac_from_smiles(self.data_dict['Smiles'][index]) > hac_filter:
                            continue
                    if use_mean:
                        value += self.data_dict['Standard Value'][index]
                        count += 1
                    else:
                        value = self.data_dict['Standard Value'][index]
                        f.write("{} {} {}\n".format(mol_id, value, i))
                if use_mean:
                    if count == 0:
                        continue
                    value /= count
                    f.write("{} {}\n".format(mol_id, value))

    def get_assay_descriptions(self):
        assay_descr = set()
        for mol_id in self.index_dict:
            for index in self.index_dict[mol_id]:
                assay_descr.add(self.data_dict['Assay Description'][index])
        return assay_descr

