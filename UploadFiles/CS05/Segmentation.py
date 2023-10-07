import os
from sympy import divisors
from sympy import isprime
from .SQLCon import *
import random
from Crypto.Cipher import AES
import hashlib
from django.contrib import messages
from django.shortcuts import redirect


class Securiti:
    def __init__(self, request, file_path,file_name, ext, mode,  type_size,nodes_dict):
        self.request = request
        self.user_name = self.request.user.username
        self.file_name = file_name
        self.ext = ext.lower()
        self.mode = mode
        self.type_size = type_size
        self.file_path = file_path
        path = os.path.abspath(self.file_path)
        self.file_stats = os.stat(path)
        if self.file_stats.st_size <= 1000000:  #1000000 size in byte
            self.file_size = self.file_stats.st_size   # for file less than 1 mb
        else:
            self.file_size = (self.file_stats.st_size / 1024)
        self.nodes_dict = nodes_dict
        # 2: ['192.168.0.102', '18b116cs']                    3: ['192.168.0.103', 'afeefa4800']}
        self.no_of_parts = 0
        self.hostdata = []

    @property
    def __fx_segment_size(self):
        file_size = self.file_size
        while isprime(file_size):
            file_size += 1
        divisors_n = divisors(int(file_size))
        divisors_n= divisors_n[:11]
        random_divisor = 0
        while random_divisor >= 5 or random_divisor <= 2:
            random_divisor = random.randint(1, len(divisors_n))
        self.no_of_parts = random_divisor
        # messages.success(self.request,"File Uploading: Total {} segments".format(self.no_of_parts))
        if self.file_stats.st_size <= 1000000:
            segment_size = (file_size / random_divisor)
        else:
            segment_size = (file_size / random_divisor) * 1024
        return int(segment_size)

    def deletesegments(self, file_id):
        try:

            for key, node in self.nodes_dict.items():
                error_value = check_all_req_server_online(node[0],node[1],node[2])
                if error_value == 1:
                    messages.error(self.request,"Server {} not online".format(key))
                    return error_value

            for key, node in self.nodes_dict.items():
                deleteblob(node[0], node[1], self.user_name, self.file_name, node[2])
                # if os.path.exists("private_key" + str(file_id) + ".txt"):
                #     os.remove("private_key" + str(file_id) + ".txt")

                # if os.path.exists(str(file_id) + "hostinfo.txt"):
                #     os.remove(str(file_id) + "hostinfo.txt")

                if os.path.exists(self.file_path):
                    os.remove(self.file_path)

                else:
                    print("The file does not exist")
            return error_value
        except KeyError:
            pass



    def get_NoOfsegments(self):
        servers = []
        value = []
        admin_record = []
        server_online = 0

        # for i in range(1, len(self.nodes_dict) + 1):
        #     addIndex = 0
        #     while(True):
        #         try:
        #             node = self.nodes_dict[i+addIndex]
        #             break
        #         except KeyError:
        #             addIndex += 1

        for key, node in self.nodes_dict.items():
            val, record = serverdata(node[0], node[1], node[2])

            if val != 'none':
                value.append(val)
            if val != 'none':
                server_online += 1
                servers.append('Server {}'.format(key))
            elif val == 'none':

                value.append(val)
                servers.append('Server {} Offline'.format(key))
            elif server_online == 0:
                servers.append("No Server")

            if record != list[0,0] :
                for j in record:
                    admin_record.append(j)


        return servers, value, server_online, admin_record


    def get_userStorage(self):
        totalval = 0
        ext_record = []
        # for i in range(1, len(self.nodes_dict) + 1):
        #     try:
        #         node = self.nodes_dict[i]
        #     except KeyError:
        #         node = self.nodes_dict[i + 1]

        for key, node in self.nodes_dict.items():
            val, record = userdata(node[0], node[1], node[2], [self.user_name])
            if val != None:
                totalval = totalval + val
            if record != list[0,0] :
                for j in record:
                    ext_record.append(j)

        return totalval, ext_record

    def get_userStorage_byadmin(self,user):
        totalval = 0
        ext_record = []
        # for i in range(1, len(self.nodes_dict) + 1):
        #     try:
        #         node = self.nodes_dict[i]
        #     except KeyError:
        #         node = self.nodes_dict[i + 1]

        for key, node in self.nodes_dict.items():
            val, record = userdata(node[0], node[1], node[2], [user])
            if val != None:
                totalval = totalval + val
            if record != list[0,0] :
                for j in record:
                    ext_record.append(j)

        return totalval, ext_record

    def aes_encrypt(self, __key, plaintext, node_no, node, file_number,file_id):
        if self.mode == 0:
            w_node_no, value = insertblob(node_no, node[0], node[1], self.user_name, self.file_name,
                                          self.ext, plaintext, file_number, node[2], None, None)
            return w_node_no, value
        elif self.mode == 2:
            user_code = open("user_code.txt", 'r')
            user_code = user_code.read()
            code = "\nresult = encryption('''{}''')".format(plaintext.decode('utf-8'))
            namespace = {}
            ciphertext = exec(user_code + code, namespace)
            ciphertext = namespace.get('result')
            w_node_no, value = insertblob(node_no, node[0], node[1], self.user_name, self.file_name,
                                          self.ext, ciphertext.encode('utf-8'), file_number, node[2], None, None)

            return w_node_no, value
        elif self.mode == 1:
            try:
                encobj = AES.new(__key, AES.MODE_GCM)
                nonce = encobj.nonce
                ciphertext, authtag = encobj.encrypt_and_digest(plaintext)

                encobj = AES.new(__key, AES.MODE_GCM, nonce)
                encobj.decrypt_and_verify(ciphertext, authtag)
            finally:
                w_node_no, value = insertblob(node_no, node[0], node[1], self.user_name,
                                              self.file_name, self.ext, ciphertext, file_number, node[2], nonce,
                                              authtag)
                return w_node_no, value
        else:
            print("Invalid mode selected")

    def decrypt(self, node, file_number,file_id,__key):
        # Read the rest of the data and get ciphertext, nonce and authtag
        ciphertext, nonce, authtag, error = readblob(node[0], node[1], self.user_name, self.file_name, file_number, node[2])
        if error == 0:
            encobj = AES.new(__key, AES.MODE_GCM, nonce)
            return encobj.decrypt_and_verify(ciphertext, authtag),error
        else:
            return ciphertext,error

    def __fx_segemts(self,file_id,__password,MyFileUpload):
        chunk_size = self.__fx_segment_size
        file_number = 1
        __key = hashlib.sha256(__password.encode()).digest()
        with open(self.file_path, "rb") as f:
            chunk = f.read(chunk_size)
            while chunk:
                if len(self.nodes_dict) == 0:
                    messages.error(self.request,"No Server Active")
                    return value
                else:
                    nodeno = random.choice(list(self.nodes_dict))
                    node = self.nodes_dict[nodeno]
                    w_node_no,value = self.aes_encrypt(__key, chunk, nodeno, node, file_number,file_id)
                    while value == 1:
                        if w_node_no in self.nodes_dict:
                            del self.nodes_dict[w_node_no]
                            if len(self.nodes_dict) == 0:
                                print("No server")
                                break
                            nodeno = random.choice(list(self.nodes_dict))
                            node = self.nodes_dict[nodeno]
                            w_node_no,value = self.aes_encrypt(__key, chunk, nodeno, node, file_number,file_id)
                    if value == 0:
                        self.hostdata.append(w_node_no)
                        progressupdate = min(100, int((file_number / self.no_of_parts) * 100))
                        MyFileUpload.objects.filter(user=self.user_name, id=self.file_name, status="Uploaded").update(progress=progressupdate)
                    file_number += 1
                    if file_number == self.no_of_parts:
                        chunk = f.read(chunk_size+2000)
                    else:
                        chunk = f.read(chunk_size)
        return value



    def __vr_segments(self,file_id,__password):
        file_number = 1
        with open(self.file_name, "rb") as f:
            rem_file_size = self.file_size
            chunk_size = random.randint(0, int(rem_file_size/2))
            rem_file_size = rem_file_size - chunk_size
            __key = hashlib.sha256(__password.encode()).digest()
            chunk = f.read(chunk_size)
            while chunk:
                nodeno = random.choice(list(self.nodes_dict))
                node = self.nodes_dict[nodeno]
                w_node_no = self.aes_encrypt(__key, chunk, nodeno, node, file_number,file_id)
                self.hostdata.append(w_node_no)
                messages.success(self.request,"Segment {} uploaded out of {} segments".format(file_number,self.no_of_parts))
                file_number += 1
                chunk_size = random.randint(0, int(rem_file_size))
                if chunk_size <= 500000:  #500000 size in byte
                    chunk_size = 500000
                rem_file_size = abs(rem_file_size - chunk_size)
                chunk = f.read(chunk_size)
        print("Data Segmented Successfully")
        print(self.hostdata)

    def segmentation(self,file_id,__password,MyFileUpload):
        if self.type_size == "fixed":
            error = self.__fx_segemts(file_id,__password,MyFileUpload)
            return self.file_stats.st_size,error
        elif self.type_size == "variable":
            self.__vr_segments(file_id,__password)
        else:
            print("Invalid mode to segment data")


    def desegment(self, host_data,file_id,__password):
        index = 0
        file_number = 1
        no_of_parts = len(host_data)
        with open(self.file_path, "wb+") as new_created_file:
            while file_number <= no_of_parts:
                nodeno = host_data[index]
                node = self.nodes_dict[nodeno]
                if self.mode == 0:
                    segment, nonce, authkey, error = readblob(node[0], node[1], self.user_name,
                                                       self.file_name, file_number, node[2])

                elif self.mode == 1:
                    __key = hashlib.sha256(__password.encode()).digest()
                    segment, error = self.decrypt(node, file_number, file_id,__key)
                else:
                    print("Invalid mode to decrypt")

                if error == 0:
                    new_created_file.write(segment)
                    file_number += 1
                    index += 1
                else:
                    return error,nodeno
        return error,nodeno

    def user_desegment(self, host_data, __key):
        index = 0
        file_number = 1
        no_of_parts = len(host_data)
        with open(self.file_path, "wb+") as new_created_file:
            while file_number <= no_of_parts:
                nodeno = host_data[index]
                node = self.nodes_dict[nodeno]
                ciphertext, nonce, authtag, error = readblob(node[0], node[1], self.user_name, self.file_name, file_number,
                                                      node[2])
                if error == 0:
                    user_code = open("user_code.txt", 'r')
                    user_code = user_code.read()
                    try:
                        code = "\nresult = decryption('''{}''')".format(ciphertext)
                        namespace = {}
                        exec(user_code + code, namespace)
                        segment = namespace.get('result')
                        new_created_file.write(segment)
                    except :
                        print('there')
                        code = "\nresult = decryption('''{}''')".format(ciphertext.decode('utf-8'))
                        namespace = {}
                        exec(user_code + code, namespace)
                        segment = namespace.get('result')
                        new_created_file.write(segment.encode('UTF-8'))
                    file_number += 1
                    index += 1
                else:
                    return error, nodeno
        return error, nodeno