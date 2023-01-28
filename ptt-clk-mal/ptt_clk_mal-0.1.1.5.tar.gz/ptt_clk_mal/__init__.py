import ptt_clk_mal.pc_clk as pc_clk
import ptt_clk_mal.pc_his as pc_his
import ptt_clk_mal.pc_parser as pc_parser
import ptt_clk_mal.pc_set as pc_set
import ptt_clk_mal.pc_dao as pc_dao

if __name__ == "__main__":
    pc_set.init_settings()
    pc_dao.create_table()
    print("All conf done!Enjoy!")



