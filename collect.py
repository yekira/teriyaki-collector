import os
import subprocess
import json

def nkf(data):
    result1 = subprocess.run(['cat'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=data.encode('utf-8'))
    result2 = subprocess.run(['nkf', "-w"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=result1.stdout)
    return result2.stdout.decode('utf-8')

path_array_list = []

def read_tja_files(path):
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isdir(full_path):
            read_tja_files(full_path)
        elif filename.endswith('.tja'):
            with open(full_path, 'r') as f:
                # do something with the file
                print("Reading %s" % full_path)
                data = nkf(f.read())

                song_file = None

                for line in data.splitlines():
                    #print(list(line))

                    if line.startswith("WAVE"):
                        tja_parent = os.path.dirname(full_path)
                        #strip() is bad?
                        sfn = line.split(':')[1].strip()

                        # HARD CODING
                        if sfn == "哀 want U(等速).ogg":
                            sfn = "哀 want U.ogg"
                        elif sfn == "太鼓の達人2020 本家終焉の最恐メドレー100(+2).ogg":
                            sfn = "太鼓の達人2020 本家終焉の最恐メドレー100.ogg"

                        song_file = os.path.join(tja_parent, sfn)
                        if not os.path.isfile(song_file):
                            print(list(song_file))
                            raise FileNotFoundError("The song file of %s does not exist." % full_path)
                        path_array = [full_path, song_file]
                        #print(path_array)
                        path_array_list.append(path_array)
                        break

                if song_file == None:
                    raise ValueError("Please define WAVE line in %s ." % full_path)

    return path_array_list

read_tja_files('flat')

# Example usage
hash_array_list = []

for tja_file, song_file in path_array_list:
    awww = []

    for some_file in [tja_file, song_file]:
        result = subprocess.run(['ipfs', 'add', '--pin', some_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Print the stdout output
        stdout_result = result.stdout.decode('utf-8')
        ipfs_cid = stdout_result.splitlines()[0].split()[1]
        if not (ipfs_cid.startswith("Qm") or ipfs_cid.startswith("bafy")):
            raise ValueError("Unknown IPFS CID: %s" % ipfs_cid)
        print(some_file, "=>", ipfs_cid)
        awww.append(ipfs_cid)

    hash_array_list.append(awww)

sorted_list = sorted(hash_array_list, key=lambda x: x[0])

print(sorted_list)

with open(os.environ["OUT"], 'w') as f:
    # Write the list to the file as JSON
    json.dump(sorted_list, f)
