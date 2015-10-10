echo "Welcome to Zepeng Guan's PS2 programming assignment."
echo "All output files will be found in this folder."
echo "Q4: Generating a new training file with rare words marked..."
python count_cfg_freq.py parse_train.dat > cfg.counts
echo "---count file generated."
python q4.py cfg.counts parse_train.dat > parse_train_rare.dat
echo "---new training file generated."
python count_cfg_freq.py parse_train_rare.dat > cfg.rare.counts
echo "---new tree generated at cfg.rare.counts."
echo "Q5: Running the CKY algorithm on the development data... runtime ~2 minutes"
python cyk.py cfg.rare.counts parse_dev.dat > cky_prediction.key
echo "---prediction generated at cky_prediction.key"
python eval_parser.py parse_dev.key cky_prediction.key
python eval_parser.py parse_dev.key cky_prediction.key > cky_eval.txt
echo "---evaluation generated at cky_eval.txt"

echo "Q6: Running the verticalized CKY algorithm on the development data..."
python count_cfg_freq.py parse_train_vert.dat > cfg.vert.counts
echo "---new count file generated."
python q4.py cfg.vert.counts parse_train_vert.dat > parse_train_vert_rare.dat
echo "---tree marked with rare words."
python count_cfg_freq.py parse_train_vert_rare.dat > cfg.vert.rare.counts
echo "---new count file generated. now running the CKY algorithm... runtime ~3 minutes"
python cyk.py cfg.vert.rare.counts parse_dev.dat > cky_vert_prediction.key
echo "---prediction generated at cky_vert_prediction.key"
python eval_parser.py parse_dev.key cky_vert_prediction.key
python eval_parser.py parse_dev.key cky_vert_prediction.key > cky_vert_eval.txt
echo "---evaluation generated at cky_vert_eval.txt"
