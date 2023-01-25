import queries
from blockInfo import Block, Analysis, Result
from ModelObject import ModelObject
import modelsFunctions
import settings


class Manager():
    settings.init()

    def set_manual_block(self, id):
        self.BLOCK = Block(id, manual=True)

    def get_info(self):
        return self.BLOCK.get_block_info()

    def set_size_value(self, stat_type):
        self.BLOCK.set_stat_type(stat_type)
        self.BLOCK.set_size_value()
        return self.BLOCK.get_scan_num(), self.BLOCK.get_block_info()["scans"]["1st"]["medium"] if self.BLOCK.get_scan_num() == 1 else self.BLOCK.get_block_info()["scans"]["2nd"]["medium"]

    def init_models(self, ids=None):
        self.MODELS = []
        self.RESULTS = []
        analysis = Analysis(blockObj=self.BLOCK)

        if ids is None:
            # create models set from automatic matching
            models = analysis.match_models()
        else:
            # create models set from ids
            models = [model for model in settings.models_objects if model.get_model_id() in ids]
            assert len(models) > 0, 'No models were chosen'
        return analysis.select_model(models, manual=True)

    def init_results(self):
        results = []
        for model in self.MODELS:
            result = Result(self.BLOCK, model)
            result.set_weights()
            results.append(result)
        return results

    def upload(self):
        assert len(self.RESULTS) == 1
        for result in self.RESULTS:
            result.save_samples(path_s3=True)

    def save_local(self):
        for result in self.RESULTS:
            result.save_dist()
            result.save_samples(path_local=True)

    def append(self, obj):
        if type(obj) is Result:
            self.RESULTS.append(obj)
        if type(obj) is ModelObject:
            self.MODELS.append(obj)

    def remove(self, obj):
        if type(obj) is Result:
            self.RESULTS.remove(obj)
        if type(obj) is ModelObject:
            self.MODELS.remove(obj)

    def get_models(self):
        list =[s for s in settings.models_objects if s.get_fruit_type() == self.get_info()['fruit_type'].lower()]
        return list

    def get_size_scale(self):
        scale = [10, 125]
        try:
            scale = settings.size_scale[self.BLOCK.get_block_info()["fruit_type"].lower()]
        except KeyError:
            print(self.BLOCK.get_block_info()["fruit_type"].lower(), " fruit type is not configured")
        finally:
            return scale

    def parser_model(self, model):
        x_scans,y_scans = self.BLOCK.get_points(model)
        return model.get_optimized_model(use_case='graph'), model.get_accumulated_days_list(), model.get_size_list(), model.get_model_formula(), model.get_labels_to_graph(),x_scans,y_scans

    @staticmethod
    def get_results(id, logger):
        # initial block object
        try:
            blockObj = Block(id=id, logger=logger)
            if blockObj.get_written_result() is not None:
                return blockObj.get_written_result(), blockObj.get_red_flag(), None, False
        except Exception as e:
            logger.error(repr(e))
            return None, True, None, False

        # initial and run analysis object
        try:
            analysis = Analysis(blockObj, logger=logger)
            size, done = analysis.run()
            result = Result(blockObj)
            result.set_weights()
            result.save_samples(path_local=True)
            result.save_dist()
        except Exception as e:
            logger.error(repr(e))
            size = None
            blockObj.set_red_flag(True)
            result = None
            done = False
        finally:
            redFlag = blockObj.get_red_flag()
            return size, redFlag, result, done

    @staticmethod
    def upload_samples(result):
        try:
            result.save_samples(path_s3=True)
        except:
            return 'Accept', '"#258a63"'
        return 'Uploaded', "#adcdb4"

    @staticmethod
    def get_projects():
        return queries.get_projects()

    @staticmethod
    def get_open_plots(id):
        return queries.get_open_plots(id)

    @staticmethod
    def get_1st_scan_plots(date):
        return queries.get_first_scan_blocks(date)

    @staticmethod
    def update_models():
        modelsFunctions.update()

    @staticmethod
    def datime_picking_date(date, refer_date):
        if date is not None and refer_date is not None:
            return Block.datime_picking_date(date, refer_date)
        else:
            return None

if __name__ == '__main__':
    M = Manager()
    c=1