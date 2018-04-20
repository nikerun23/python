# -*- coding: utf8 -*-

import sys
import logging
import os
import timeit

import cx_Oracle


class IDUpdate():

    def __init__(self, info_path, data_path):
        self.LoadDBInfo(info_path)

    def __enter__(self):
        ## DB 연결 ##
        dsn = cx_Oracle.makedsn(self.db_info['IP'], self.db_info['PORT'], self.db_info['SID'])
        self.__db = cx_Oracle.Connection(self.db_info['ID'], self.db_info['PWD'], dsn)
        self.__cursor = self.__db.cursor()
        return self

    def __exit__(self, type, value, traceback):
        ## DB 연결 종료 ##
        self.__cursor.close()
        self.__db.close()

    def LoadListFile(self, path, output):
        with open(path) as f:
            for line in f:
                output.append(line.strip(' \t\r\n'))

    def LoadTsvFile(self, path, output):
        with open(path) as f:
            for line in f:
                output.append(line.strip(' \t\r\n').split('\t')[0])

    def LoadTsvFileByCol(self, path, output, col_num):
        with open(path) as f:
            for line in f:
                output.append(line.strip(' \t\r\n').split('\t')[col_num])

    def LoadDBInfo(self, path):
        with open(path) as f:
            self.db_info = load_json(f.read())

    def BackupTable(self, from_tbl, to_tbl):
        ## 기존 테이블에서 select
        try:
            backup_query = 'INSERT INTO %s SELECT * FROM %s' % (to_tbl, from_tbl)
            self.__cursor.execute(backup_query)
        except:
            raise Exception('# Query failed : %s' % backup_query)

    def DeleteTable(self, target_tbl):
        try:
            delete_query = 'DELETE FROM %s' % (target_tbl)
            self.__cursor.execute(delete_query)
        except:
            raise Exception('# Query failed : %s' % delete_query)

    def ReadCLOBData(self):
        db_data = []
        for row in self.__cursor.__iter__():
            row_data = []
            for i in xrange(len(row)):
                if type(row[i]) is cx_Oracle.LOB:
                    row_data.append(row[i].read)
                else:
                    row_data.append(row[i])
            db_data.append(tuple(row_data))

        return db_data

    def InsertTable(self, data, target_tbl):
        insert_query = 'INSERT INTO %s (FIELD_NAME1, FIELD_NAME2, FIELD_NAME3, FIELD_NAME4, FIELD_NAME5) VALUES (:1, :2, :3, :4, :5)' % (
            target_tbl)
        try:
            self.__cursor.setinputsizes(20, 4, 10, cx_Oracle.CLOB, 14)
            self.__cursor.executemany(insert_query, data)
        except:
            raise Exception('# Query failed : %s' % insert_query)



    def Process(self):
        temp = []

        with open(self.data_path) as f:
            for line in f:
                line_data = line.strip('\n').split('\t')
                if line_data[1] == 'type1':
                    line_data[3] = self.UpdateID1(line_data[3])
                elif line_data[1] == 'type2':
                    line_data[3] = self.UpdateID2(line_data[3])

                if line_data[3] == None:
                    continue

                temp.append(tuple(line_data))

        try:
            self.__db.begin()
            self.DeleteTable('백업테이블명')
            self.BackupTable('테이블명', '백업테이블명')
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            logging.error(str(e))
            sys.exit(-1)

        try:
            self.__db.begin()
            self.DeleteTable('테이블명')
            self.InsertCartTable(temp, '테이블명')
            self.__db.commit()
        except Exception as e:
            self.__db.rollback()
            logging.error(str(e))
            sys.exit(-1)

    def DownloadTable(self, target_tbl):
        try:
            select_query = 'SELECT * FROM %s' % (target_tbl)
            self.__cursor.execute(select_query)
        except:
            logging.debug('# Query failed : %s' % select_query)
        try:
            for data in self.__cursor.__iter__():
                temp = ''
                col_size = len(data)
                for i in xrange(col_size):
                    if type(data[i]) is cx_Oracle.LOB:
                        temp += data[i].read()
                    else:
                        temp += data[i]
                    if i < col_size - 1:
                        temp += '\t'
                print
                temp
        except:
            logging.debug('# DB cursor error')


#
# main
#
if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding('utf8')
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    os.putenv('NLS_LANG', '.UTF8')

    start_time = timeit.default_timer()

    if len(sys.argv) == 3:
        info_path, data_path = sys.argv[1:]
    else:
        logging.info('usage) %s info_path data_path' % sys.argv[0])
        logging.info('  ex) %s db_info.json data.tsv' % sys.argv[0])
        sys.exit(-1)

    with Updater(info_path, data_path) as updater:
        updater.Process()

    logging.debug('# Processing time: %s seconds' % str(round(timeit.default_timer() - start_time, 9)))
    logging.debug('# Memory usage : %s MB' % str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000))

    sys.exit(0)
