<?php
	session_start();

$tarifs_hebdo_profil = array("MILIMA", "ANGWIN_HEBDO", "CUVFAU", "MAISOB");

$tarifs_hebdo_chemin = array("MILLESIMA", "ANGWIN_HEBDO", "CUVFAU", "MAISOB");

/*
$tarifs_hebdo_profil = array(
    "MILIMA" => "MILLESIMA",
    "ANGWIN_HEBDO" => "ANGWIN_HEBDO",
    "CUVFAU"   => "CUVFAU",
    "MAISOB"  => 100,
);*/

$chemin_fichiers_php = "/var/www/html/php/";

//$chemin_fichiers_php = "/php/";
//$chemin_fichiers_php = "./html/php/";

foreach ($tarifs_hebdo_profil as $key => $profil){

    echo "test2.php";

    echo "   ";

    $chemin_traitement = $chemin_fichiers_php . $tarifs_hebdo_chemin[$key] . "/";

    echo ($chemin_traitement . "traitement_" . $profil . ".py");

    echo "   ";

    // Execution du script python adéquate au profil du tarif.
	//$script_tarif = basename($chemin_traitement . "traitement_" . $profil . ".py");
    //$script_tarif = basename("../test.php");
    //$script_tarif = basename("/Volumes/Intranet/Tarifs/batchs/test.php");

    //$script_tarif = "/Volumes/Intranet/Tarifs/batchs/test.php";
    //$script_tarif = "/var/www/html/Tarifs/batchs/test.php";

    $script_tarif = "/var/www/html/Tarifs/batchs/test2.py";


    echo "   ";

	echo shell_exec('python3 ' . $script_tarif . ' 2>&1');
    //echo shell_exec('php -f ' . $script_tarif . ' 2>&1');

    echo "   ";

    //$chemin_fichier_sortie = $chemin_fichiers_php . "tarifs_HEBDO/";

    //echo ($chemin_fichier_sortie . "sortie_" . $profil . ".xlsx");

    //echo "   ";

	//$file_OUT=basename($chemin_fichier_sortie . "sortie_" . $profil . ".xlsx");
}
?>

$tab_profil = ["ARTHUR", "ADEX", "ANGWIN_BXOWC", "ANGWIN_BDXNOTOWC", "ANGWIN_BGO", "ANGWIN_AUTRES", "ARTY", "ARVI", "BORBLE", "BORBLE2", "BORDIN", "BPCWIN",
"CEPAGE", "CAVMAR", "CAVTOU", "CDFINT", "CDP", "CDP2", "CDP4", "CERSTE", "CHACHA", "CHACOM", "COMVIG", "CRUCOL", "DUBOS", "ENCVIN",
"ENSEI", "ENSEI2", "FARR", "FILIPS", "INFO", "LABERG", "LABERG2", "MILLE1", "MILLES", "MILLES2", "MONTAG", "NISIMA",
"PIONSA", "RGRD", "SOBOVI", "SODIVI", "TERTRA", "TRANSV", "VGC", "WILKIN", "WINARO", "WINEMA", "BOUOFF", "DESCAF",
"PASTER", "CAVHUG", "GABIN", "JSCD", "ALIOFF", "IN2WIN", "GINOFF", "CLOMIL", "SOBOFF", "QUACOU", "QUACOU2",
"QUACOU3", "QUACOU4", "QUACOU5", "CMVINS", "BALOFF", "BARIOF", "CDFOFF", "TWMOFF", "COMOFF", "ARIVOF", "JOHNOF",
"LVDCOF", "VIALOF", "VINONE", "BONCHA", "VERSUS", "SWIT", "VEYLOF", "VEYLOF2", "DEWITT", "DEWITT2", "DEWITT3",
"ENSEI3", "OENOE", "STATEV", "CLOMIL2", "CLOMIL3", "VGC2", "SICHE2", "OENALI", "MILLES3", "CDP3", "BOUEY",
"ANGWIN2", "CUVFAU", "TWINOF", "CAVCAR", "CAVCAR2", "CAVEX", "VINTEX", "CRSFW", "NGVINS", "EXTRACT_BORDEREAUX",
"MARSOI", "JOEMEY", "YVMOFF", "MORTIE", "REDCIR"]


//redirect.php
<?php
//session_start();
//	$_SESSION['profil'] = $_POST['tarif'];

if ($_SESSION['profil']=='TRANSV')
	{
		echo '
			<html>
				<head>
					<meta charset="utf-8" />
					<title>TRANSVIN</title>
				</head>
				<body>
					<form method="post" action="TRANSV/script.php">
					<input type="submit" value="Lancer traitement TRANSVIN" />
					</form>
				</body>
			</html>';
	}

    foreach ($tab_profil as $profil){

        if ($_SESSION['profil'] == $profil)
        {
            echo '
                    <html>
                            <head>
                                    <meta charset="utf-8" />
                                    <title>' . $profil . '</title>
                            </head>
                            <body>
                                    <form method="post" action='$profil . '/script.php">
                                    <input type="submit" value="Lancer traitement ' . $profil  . ' CELLAR" />
                                    </form>
                            </body>
                    </html>';
        }
    }
?>

//upload.php
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="../style.css" />
		<title>INTRANET BLQ</title>
	</head>
<div id="bloc_page">
<?php
	session_start();
	include('../header.html');
	include('../menu.html');
?>

    <?php
	session_start();

	// Vérifier que le formulaire a été soumis
	if ($_SERVER["REQUEST_METHOD"] == "POST")
	{
		//Vérifie si le fichier a été uploadé sans erreur.
		if(isset($_FILES["tarifupload"]) && $_FILES["tarifupload"]["error"] == 0)
		{
			//$allowed = array("csv" => "/tmp/php/");
			$allowedExt = array("csv", "xls", "xlsx");
			$allowedMime = array("text/csv", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel");
			$filename = $_FILES["tarifupload"]["name"];
			$filetype = $_FILES["tarifupload"]["type"];
			$filesize = $_FILES["tarifupload"]["size"];
			$_SESSION['charged'] = '1';

			// Vérifie l'extension du fichier
			$ext = pathinfo($filename, PATHINFO_EXTENSION);
			//if (!array_key_exists($ext, $allowed)) die("Erreur : Votre fichier n'est pas au format csv (utf-8). Merci de l'enregistrer au bon format avant de le charger.");
			if (!in_array($ext, $allowedExt)) die("Erreur : Votre fichier n'est pas au format au bon format. (csv utf-8, xls ou xlsx uniquement).");
			// Verifie la taille du fichier - 10Mo Maximum
			//$maxsize = 10 * 1024 * 1024;
			//if($filesize > $maxsize) die("Error: La taille du fichier est supérieure à la limite autorisée.");

			// Verifie le type MIME du fichier
			if (in_array($filetype, $allowedMime))
			{
                // Verifie si le fichier existe avant de le télécharger.
                foreach ($tab_profil as $profil){
                    if ($_SESSION['profil'] == $profil)
                    {
                        if(file_exists($profil . "/" . $_FILES["tarifupload"]["name"]))
                        {
                            echo $_FILES["tarifupload"]["name"] . " existe déjà.";
                        }
                        else
                        {
                            move_uploaded_file($_FILES["tarifupload"]["tmp_name"], $profil . "/" . $_FILES["tarifupload"]["name"]);
                            echo "votre fichier a été téléchargé avec succès.";
                        }
                    }
                }
            }
			else
			{
				echo "Error: Il y a eu un probème de téléchargement de votre fichier. Veuillez réessayer.";
			}
		}
		else
		{
			echo "Error: " . $_FILES["tarifupload"]["error"];
			$_SESSION['charged'] = '0';
		}
	}
	include("redirect.php");
	<br>
    ?>
		<input type="button" onclick="window.location.href='/traitement_tarifs.php'"; value="TRAITER UN NOUVEAU TARIF" />
	</section>
</body>
</html>
