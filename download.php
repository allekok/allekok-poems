<?php
/* 
 * دابەزاندنی شێعرەکانی ئاڵەکۆک
 * بۆ زانیاری زیاتر سەردانی لاپەڕەی خوارەوە بکەن:
 * https://allekok.ir/dev/tools/
 */
/* Constants */
const __POEMS_DIR = "شێعرەکان";

/* Run */
دابەزاندنی_هەموو_شێعرەکان();

/* Functions */
function download_poets_info($poet_id)
{
    $url = "https://allekok.ir/dev/tools/poet.php?poet=$poet_id";
    while(!$json = json_decode(file_get_contents($url), true))
    {
        sleep(1);
    }
    echo "Poets info downloaded.\n\n";
    return $json;
}

function دابەزاندنی_هەموو_شێعرەکان()
{
    global $argv;
    $arg = @$argv[1] ? $argv[1] : 'all';
    $poets = download_poets_info($arg);

    foreach($poets as $poet)
    {
        foreach($poet['bks'] as $i=>$book)
        {
            $encoded_bk = urlencode($book);
            $book = str_replace("/", "-", $book);
            $path = __POEMS_DIR . "/" . $poet['profname'] . "/" . $book;
            check_mkdir($path);

            /* Comment: دابەزاندنی شێعرەکان */
            $poems_uri = "https://allekok.ir/dev/tools/poem.php?poet=" .
			 $poet['id'] . "&book=" . $encoded_bk . "&poem=all";
            while(!$poems = json_decode(file_get_contents($poems_uri)
                ,true)["poems"])
            {
                sleep(1);
            }
            echo "Poet: ".$poet["id"]."\tBook: ".($i+1)."\tPoems downloaded.\n";

            /* Comment: پاشەکەوت کردنی شێعرەکان */
            $max_file_name_length = 50;
            
            for($i=0; $i<count($poems); $i++)
            {
                $poems[$i]["hon"] = str_replace(["\r","&#39;","&#34;","&laquo;","&raquo;","  ","   ","    "],
                                                ["","'","\"","«","»"," "," "," "],$poems[$i]["hon"]);
                $poems[$i]["hon"] = preg_replace("/\n\n+/u", "\n\n", $poems[$i]["hon"]);
                $poems[$i]["hon"] = trim($poems[$i]["hon"]);
                $poems[$i]["name"] = trim($poems[$i]["name"]);
                $filename = kurdish_numbers($poems[$i]["id"]) . ". " .
			    mb_substr(str_replace(["/","."], ["-",""], $poems[$i]["name"]),
				      0, $max_file_name_length);
                $towrite  = "شاعیر: " . $poet["profname"];
                $towrite .= "\nکتێب: " . $book;
                $towrite .= "\nسەرناو: " . $poems[$i]["name"];
                if(trim($poems[$i]["hdesc"]))
                {
		    $poems[$i]["hdesc"] = str_replace("<br>", " - ", $poems[$i]["hdesc"]);
		    $poems[$i]["hdesc"] = preg_replace("/\s\s+/u", " ", $poems[$i]["hdesc"]);
		    $poems[$i]["hdesc"] = filter_var($poems[$i]["hdesc"],
						     FILTER_SANITIZE_STRING);
		    $poems[$i]["hdesc"] = trim($poems[$i]["hdesc"]);
		    $towrite .= "\nلەبارەی شێعر: " . $poems[$i]["hdesc"];
                }
		$towrite .= "\n\n";
		$towrite .= $poems[$i]["hon"];
		file_put_contents($path . "/" . $filename, $towrite);
	    }
	}
    }
}

function check_mkdir($path)
{
    if(!file_exists($path))
	mkdir($path, 0755, true);
}

function kurdish_numbers($string)
{
    return str_replace(['0','1','2','3','4','5','6','7','8','9'],
		       ['٠','١','٢','٣','٤','٥','٦','٧','٨','٩'],
		       $string);
}
?>
