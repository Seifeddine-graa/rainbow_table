import Tools 
import pickle as pk
import tqdm 
#longueur des chaines arc-en-ciel
chains_length=256
#taille de la table arc-en-ciel
rainbow_table_size=10_000_000
def compute_chain(password)->tuple :
    """
    Calcule une chaine arc_en_ciel
    
    :param password: le mot de passe de départ (str)
    :return: password et dernier hash obtenu à la dernière ittération
    :rtype: tuple
    """
    password_intermediaire=password
    for i in range(1,chains_length):
        hash=Tools.md5_hash(password_intermediaire)
        password_intermediaire=Tools.reduce(hash,i)
    hash=Tools.md5(password_intermediaire)
    return(password,hash)
def compute_rainbow_table():
    """
    Calcule la table arc_en_ciel
    """
    database={}
    # Génération de la table arc-en-ciel
    for i in tqdm.tqdm(range(rainbow_table_size),desc="génération table arc-en-ciel"):
        init_password=Tools.generate_password()
        passwd,final_hash =compute_chain(init_password)
        #Si le hash n'éxiste pas déjà                          #ou 
        if final_hash not in database:                         # |if final_hash not in database:  
            database[final_hash]=[]                            # |     database[final_hash]=[]      
            database[final_hash].append(init_password)         # |database[final_hash].append(init_password)
        #Sinon le hash existe déjà                             # comme çà on évite de écrire la ligne de code else ...
        else:
            database[final_hash].append(init_password)
    #Sauvegarder avec pickle
    with open("rainbow_table_1.pkl","wb") as file:
        pk.dump(database,file)
    print(f'Table arc-en-ciel sauvegardée({len(database)}) entrées')
    return database
def load_rainbow_table():
    """
    Charge la table arc_en_ciel depuis le fichier
    """
    with open("rainbow_table_1.pkl","rb") as file:
        return pk.load(file)
#compute_rainbow_table()
def crack_password(target_hash: str, database: dict) -> str:
    """
    Logique de recherche Arc-en-Ciel (Rainbow Table Search).
    On cherche si le hash cible peut se trouver dans l'une des chaînes.
    """
    # On itère de la fin vers le début
    for i in range(chains_length - 1, -1, -1):
        
        # On construit la 'queue' de la chaîne candidate
        # On part du hash cible, on applique R_i, puis H, puis R_{i+1}...
        # pour tomber potentiellement sur un hash final présent dans la table
        current_hash = target_hash
        
        for j in range(i+1, chains_length):
            current_pwd = Tools.reduce(current_hash, j)
            current_hash = Tools.md5_hash(current_pwd)
            
        # On regarde si ce hash final (calculé) est dans la table
        if current_hash in database:
            # Si oui, on regarde tous les mots de passe de départ qui mènent à cette fin
            for start_pwd in database[current_hash]:
                
                # On recalcule la chaîne en entier depuis le début pour trouver le match exact
                current_hash = Tools.md5_hash(start_pwd)
                for j in range(1, chains_length):
                    if current_hash == target_hash:
                        return start_pwd # Trouvé !
                    
                    current_pwd = Tools.reduce(current_hash, j)
                    current_hash = Tools.md5_hash(current_pwd)
                    
    return None # Pas trouvé
dico=load_rainbow_table()
def simulation(n):
    cracked_passwords=0
    for i in tqdm.tqdm(range(n)):
        hash1 = Tools.md5_hash(Tools.generate_password())
        result = crack_password(hash1, dico)
        if isinstance(result, str):
            cracked_passwords += 1
    print(f"{cracked_passwords} cracked passwords and {n - cracked_passwords} uncracked passwords")
simulation(500)

