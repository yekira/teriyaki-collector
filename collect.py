import os
import chardet
import subprocess
import json

path_array_list = []

def read_tja_files(path):
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isdir(full_path):
            read_tja_files(full_path)
        elif filename.endswith('.tja'):
            with open(full_path, 'rb') as f:
                # do something with the file
                data = f.read()
                encoding = chardet.detect(data)["encoding"]
                print("Reading %s as %s" % (full_path, encoding))
                new_data = data.decode(encoding)

                song_file = None

                for line in new_data.splitlines():
                    print(list(line))

                    if line.startswith("WAVE"):
                        tja_parent = os.path.dirname(full_path)
                        #strip() is bad?
                        song_file = os.path.join(tja_parent, line.split(':')[1].strip())
                        if not os.path.isfile(song_file):
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

with open('output.json', 'w') as f:
    # Write the list to the file as JSON
    json.dump(sorted_list, f)
