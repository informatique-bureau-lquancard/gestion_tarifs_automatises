class Profil:
    def __init__(self, id, profil, chemin, flux, type_profil, description_flux, nom_flux, type_flux):
        self.id = id
        self.profil = profil
        self.chemin = chemin
        self.flux = flux
        self.type_profil = type_profil
        self.description_flux = description_flux
        self.nom_flux = nom_flux
        self.type_flux = type_flux
    
    def get_id(self):
            return self.__id

    def set_id(self, id):
        self.__id = id

    def get_profil(self):
        return self.__profil

    def set_profil(self, profil):
        self.__profil = profil

    def get_chemin(self):
        return self.__chemin

    def set_chemin(self, chemin):
        self.__chemin = chemin

    def get_flux(self):
        return self.__flux

    def set_flux(self, flux):
        self.__flux = flux

    def get_type_profil(self):
        return self.__type_profil

    def set_type_profil(self, type_profil):
        self.__type_profil = type_profil
    
    def get_type_description_flux(self):
        return self.__description_flux

    def set_description_flux(self, description_flux):
        self.__description_flux = description_flux

    def get_nom_flux(self):
        return self.__nom_flux

    def set_nom_flux(self, nom_flux):
        self.__nom_flux = nom_flux

    def get_type_flux(self):
        return self.__type_flux

    def set_type_flux(self, type_flux):
        self.__type_flux = type_flux

