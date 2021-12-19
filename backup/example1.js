// Create Dialog Box
var Dialog = new DzDialog();
Dialog.width = 390;
Dialog.height = 721;
Dialog.caption = "";

// Create and define DzLabel: 'billboardCreatorTitle'
var billboardCreatorTitle = new DzLabel( Dialog );
billboardCreatorTitle.setGeometry( 0, 0, 401, 41 );
billboardCreatorTitle.text = "Billboard Creator";

// Create tab stack
var tabWidget = new DzTabWidget( Dialog );
tabWidget.setGeometry( 20, 40, 361, 601 );
tabWidget.currentIndex = 0;
tabWidget.tabPosition = DzTabWidget.North;

// Add tab page 'Setup'
var setupTab = new DzWidget( tabWidget );
setupTab.setGeometry( 20, 40, 361, 601 );
tabWidget.addTab( setupTab, 'Setup' );

// Add tab page 'Post-Render Setup'
var postRenderSetupTab = new DzWidget( tabWidget );
postRenderSetupTab.setGeometry( 20, 40, 361, 601 );
tabWidget.addTab( postRenderSetupTab, 'Post-Render Setup' );

// Add tab page 'Quick Help'
var quickHelpTab = new DzWidget( tabWidget );
quickHelpTab.setGeometry( 20, 40, 361, 601 );
tabWidget.addTab( quickHelpTab, 'Quick Help' );

// Create and define DzGroupBox: 'outputBox'
var outputBox = new DzGroupBox( setupTab );
outputBox.setGeometry( 0, 9, 351, 51 );
outputBox.title = 'Output Folder';
outputBox.orientation = DzWidget.Vertical;

// Create and define DzComboBox: 'outputFolderBox'
var outputFolderBox = new DzComboBox( setupTab );
outputFolderBox.setGeometry( 10, 29, 331, 22 );

// Create and define DzGroupBox: 'imgBaseNameBox'
var imgBaseNameBox = new DzGroupBox( setupTab );
imgBaseNameBox.setGeometry( 0, 60, 351, 51 );
imgBaseNameBox.title = 'Image Base Name';
imgBaseNameBox.orientation = DzWidget.Vertical;

// Create and define DzLineEdit: 'imageLineEdit'
var imageLineEdit = new DzLineEdit( setupTab );
imageLineEdit.setGeometry( 10, 80, 331, 22 );
imageLineEdit.text = "";

// Create and define DzGroupBox: 'previewBox'
var previewBox = new DzGroupBox( setupTab );
previewBox.setGeometry( 0, 470, 351, 91 );
previewBox.title = 'Preview';
previewBox.orientation = DzWidget.Vertical;

// Create and define DzLabel: 'vertical'
var vertical = new DzLabel( setupTab );
vertical.setGeometry( 20, 500, 42, 16 );
vertical.text = "Vertical";

// Create and define DzIntSlider: 'verticalSlider'
var verticalSlider = new DzIntSlider( setupTab );
verticalSlider.setGeometry( 76, 498, 271, 22 );

// Create and define DzLabel: 'horizontal'
var horizontal = new DzLabel( setupTab );
horizontal.setGeometry( 12, 527, 57, 16 );
horizontal.text = "Horizontal";

// Create and define DzIntSlider: 'horizontalSlider'
var horizontalSlider = new DzIntSlider( setupTab );
horizontalSlider.setGeometry( 76, 527, 271, 22 );

// Create and define DzGroupBox: 'preRenderSettingsBox'
var preRenderSettingsBox = new DzGroupBox( setupTab );
preRenderSettingsBox.setGeometry( 0, 110, 351, 171 );
preRenderSettingsBox.title = 'Pre-Render Settings';
preRenderSettingsBox.orientation = DzWidget.Vertical;

// Create and define DzLineEdit: 'lineEdit_2'
var lineEdit_2 = new DzLineEdit( setupTab );
lineEdit_2.setGeometry( 290, 130, 41, 22 );
lineEdit_2.text = "30";

// Create and define DzLabel: 'label_3'
var label_3 = new DzLabel( setupTab );
label_3.setGeometry( 10, 130, 191, 21 );
label_3.text = "Render in degree increments of:";

// Create and define DzLabel: 'xAngleRangeText'
var xAngleRangeText = new DzLabel( setupTab );
xAngleRangeText.setGeometry( 120, 160, 101, 21 );
xAngleRangeText.text = "X Angle Range";

// Create and define DzLineEdit: 'minXLine'
var minXLine = new DzLineEdit( setupTab );
minXLine.setGeometry( 50, 160, 41, 22 );
minXLine.text = "0";

// Create and define DzLabel: 'minX'
var minX = new DzLabel( setupTab );
minX.setGeometry( 10, 160, 31, 21 );
minX.text = "Min:";

// Create and define DzLabel: 'maxX'
var maxX = new DzLabel( setupTab );
maxX.setGeometry( 250, 160, 41, 21 );
maxX.text = "Max:";

// Create and define DzLineEdit: 'maxXLine'
var maxXLine = new DzLineEdit( setupTab );
maxXLine.setGeometry( 290, 160, 41, 22 );
maxXLine.text = "300";

// Create and define DzLabel: 'maxY'
var maxY = new DzLabel( setupTab );
maxY.setGeometry( 250, 190, 41, 21 );
maxY.text = "Max:";

// Create and define DzLineEdit: 'minYLine'
var minYLine = new DzLineEdit( setupTab );
minYLine.setGeometry( 50, 190, 41, 22 );
minYLine.text = "0";

// Create and define DzLineEdit: 'maxYLine'
var maxYLine = new DzLineEdit( setupTab );
maxYLine.setGeometry( 290, 190, 41, 22 );
maxYLine.text = "180";

// Create and define DzLabel: 'yAngleRangeTxt'
var yAngleRangeTxt = new DzLabel( setupTab );
yAngleRangeTxt.setGeometry( 120, 190, 101, 21 );
yAngleRangeTxt.text = "Y Angle Range";

// Create and define DzLabel: 'minY'
var minY = new DzLabel( setupTab );
minY.setGeometry( 10, 190, 31, 21 );
minY.text = "Min:";

// Create and define DzCheckBox: 'useZchkBox'
var useZchkBox = new DzCheckBox( setupTab );
useZchkBox.setGeometry( 80, 220, 201, 20 );
useZchkBox.text = "Use Z axis as horizontal axis";
useZchkBox.checked = false;

// Create and define DzCheckBox: 'rotateFromStartChkBox'
var rotateFromStartChkBox = new DzCheckBox( setupTab );
rotateFromStartChkBox.setGeometry( 80, 250, 201, 20 );
rotateFromStartChkBox.text = "Rotate from starting rotation";
rotateFromStartChkBox.checked = false;

// Create and define DzGroupBox: 'summaryBox'
var summaryBox = new DzGroupBox( setupTab );
summaryBox.setGeometry( 0, 280, 351, 191 );
summaryBox.title = 'Summary';
summaryBox.orientation = DzWidget.Vertical;

// Create and define DzTextEdit: 'summary_text'
var summary_text = new DzTextEdit( setupTab );
summary_text.setGeometry( 10, 370, 331, 91 );

// Create and define DzLabel: 'pixmap_label'
var pixmap_label = new DzLabel( setupTab );
pixmap_label.setGeometry( 250, 300, 71, 51 );
pixmap_label.text = "";

// Create and define DzLabel: 'summaryMsg'
var summaryMsg = new DzLabel( setupTab );
summaryMsg.setGeometry( 20, 310, 71, 21 );
summaryMsg.text = "Excellent!";

// Create and define DzLabel: 'summaryMsg_2'
var summaryMsg_2 = new DzLabel( setupTab );
summaryMsg_2.setGeometry( 20, 340, 121, 16 );
summaryMsg_2.text = "You're ready to go!";

// Create and define DzGroupBox: 'postRenderBox'
var postRenderBox = new DzGroupBox( postRenderSetupTab );
postRenderBox.setGeometry( 0, 0, 351, 91 );
postRenderBox.title = 'Post-Render Settings';
postRenderBox.orientation = DzWidget.Vertical;

// Create and define DzCheckBox: 'autoGenMaskChkBox'
var autoGenMaskChkBox = new DzCheckBox( postRenderSetupTab );
autoGenMaskChkBox.setGeometry( 30, 20, 151, 20 );
autoGenMaskChkBox.text = "Auto-generate masks";
autoGenMaskChkBox.checked = false;

// Create and define DzCheckBox: 'setupBillboardChkBox'
var setupBillboardChkBox = new DzCheckBox( postRenderSetupTab );
setupBillboardChkBox.setGeometry( 30, 40, 151, 20 );
setupBillboardChkBox.text = "Setup billboard node";
setupBillboardChkBox.checked = false;

// Create and define DzCheckBox: 'skipFailedChkBox'
var skipFailedChkBox = new DzCheckBox( postRenderSetupTab );
skipFailedChkBox.setGeometry( 30, 60, 271, 20 );
skipFailedChkBox.text = "Skip failed renders / Ignore render errors";
skipFailedChkBox.checked = false;

// Create and define DzGroupBox: 'maskGenBox'
var maskGenBox = new DzGroupBox( postRenderSetupTab );
maskGenBox.setGeometry( -1, 89, 351, 231 );
maskGenBox.title = 'Mask Generation Options';
maskGenBox.orientation = DzWidget.Vertical;

// Create and define DzGroupBox: 'hardOrSoftBox'
var hardOrSoftBox = new DzGroupBox( postRenderSetupTab );
hardOrSoftBox.setGeometry( 9, 109, 331, 51 );
hardOrSoftBox.title = 'Hard Mask or Soft Mask';
hardOrSoftBox.orientation = DzWidget.Vertical;

// Create and define DzRadioButton: 'hardMaskRadio'
var hardMaskRadio = new DzRadioButton( postRenderSetupTab );
hardMaskRadio.setGeometry( 29, 129, 95, 20 );
hardMaskRadio.text = "Hard Mask";
hardMaskRadio.checked = false;
// Unhook automatic radio button exclusivity handling
hardMaskRadio.getWidget().autoExclusive = false;

// Create and define DzRadioButton: 'softMaskRadio'
var softMaskRadio = new DzRadioButton( postRenderSetupTab );
softMaskRadio.setGeometry( 229, 129, 95, 20 );
softMaskRadio.text = "Soft Mask";
softMaskRadio.checked = true;
// Unhook automatic radio button exclusivity handling
softMaskRadio.getWidget().autoExclusive = false;

// Create and define DzGroupBox: 'otherBox'
var otherBox = new DzGroupBox( postRenderSetupTab );
otherBox.setGeometry( 9, 209, 331, 101 );
otherBox.title = 'Other options';
otherBox.orientation = DzWidget.Vertical;

// Create and define DzLineEdit: 'alphaToleranceLineEdit'
var alphaToleranceLineEdit = new DzLineEdit( postRenderSetupTab );
alphaToleranceLineEdit.setGeometry( 269, 229, 51, 22 );
alphaToleranceLineEdit.text = "20";

// Create and define DzLabel: 'nProcessorsLbl'
var nProcessorsLbl = new DzLabel( postRenderSetupTab );
nProcessorsLbl.setGeometry( 39, 259, 131, 16 );
nProcessorsLbl.text = "Number of Processors: ";

// Create and define DzLabel: 'alphaToleranceLbl'
var alphaToleranceLbl = new DzLabel( postRenderSetupTab );
alphaToleranceLbl.setGeometry( 39, 229, 121, 16 );
alphaToleranceLbl.text = "Alpha Tolerance: ";

// Create and define DzLineEdit: 'processorsLineEdit'
var processorsLineEdit = new DzLineEdit( postRenderSetupTab );
processorsLineEdit.setGeometry( 269, 259, 51, 22 );
processorsLineEdit.text = "4";

// Create and define DzCheckBox: 'quietChkBox'
var quietChkBox = new DzCheckBox( postRenderSetupTab );
quietChkBox.setGeometry( 149, 279, 61, 20 );
quietChkBox.text = "Quiet";
quietChkBox.checked = false;

// Create and define DzGroupBox: 'modeBox'
var modeBox = new DzGroupBox( postRenderSetupTab );
modeBox.setGeometry( 9, 159, 331, 51 );
modeBox.title = 'Mode selection';
modeBox.orientation = DzWidget.Vertical;

// Create and define DzRadioButton: 'performanceRadio'
var performanceRadio = new DzRadioButton( postRenderSetupTab );
performanceRadio.setGeometry( 29, 179, 141, 20 );
performanceRadio.text = "Prefer Performance";
performanceRadio.checked = false;
// Unhook automatic radio button exclusivity handling
performanceRadio.getWidget().autoExclusive = false;

// Create and define DzRadioButton: 'preserveRadio'
var preserveRadio = new DzRadioButton( postRenderSetupTab );
preserveRadio.setGeometry( 199, 179, 131, 20 );
preserveRadio.text = "Preserve Memory";
preserveRadio.checked = true;
// Unhook automatic radio button exclusivity handling
preserveRadio.getWidget().autoExclusive = false;

// Create and define DzGroupBox: 'maskGenBoxOutputBox'
var maskGenBoxOutputBox = new DzGroupBox( postRenderSetupTab );
maskGenBoxOutputBox.setGeometry( 0, 320, 351, 211 );
maskGenBoxOutputBox.title = 'Mask Generator Output';
maskGenBoxOutputBox.orientation = DzWidget.Vertical;

// Create and define DzTextEdit: 'maskGenOutputTextEdit'
var maskGenOutputTextEdit = new DzTextEdit( postRenderSetupTab );
maskGenOutputTextEdit.setGeometry( 10, 340, 331, 181 );

// Create and define DzPushButton: 'retryFailedRenderBtn'
var retryFailedRenderBtn = new DzPushButton( postRenderSetupTab );
retryFailedRenderBtn.setGeometry( 10, 540, 161, 28 );
retryFailedRenderBtn.text = "Retry Failed Renders";
retryFailedRenderBtn.objectName = 'retryFailedRenderBtn';
connect( retryFailedRenderBtn, 'clicked()', clicked_retryFailedRenderBtn );

/*********************************************************************/
function clicked_retryFailedRenderBtn() {
	
}

// Create and define DzPushButton: 'retryFailedMasks'
var retryFailedMasks = new DzPushButton( postRenderSetupTab );
retryFailedMasks.setGeometry( 190, 540, 151, 28 );
retryFailedMasks.text = "Retry Failed Masks";
retryFailedMasks.objectName = 'retryFailedMasks';
connect( retryFailedMasks, 'clicked()', clicked_retryFailedMasks );

/*********************************************************************/
function clicked_retryFailedMasks() {
	
}

// Create and define DzLabel: 'helpLabel'
var helpLabel = new DzLabel( quickHelpTab );
helpLabel.setGeometry( 20, 0, 311, 181 );
helpLabel.text = "This application can be used to create billboards to help lower GPU memory and/or improve render performance while keeping your scenes crowded! This application has the capability of rendering series of images, create cutout masks, and setup billboard nodes to work in compliance w/ RiverSoftArt's Now-Crowds Billboard Scripts.   ";

// Create and define DzLabel: 'moreInfoLabel'
var moreInfoLabel = new DzLabel( quickHelpTab );
moreInfoLabel.setGeometry( 12, 470, 331, 41 );
moreInfoLabel.text = "For additional information, please refer to Billboard Creator documentation.";

// Create and define DzPushButton: 'openDocumentationBtn'
var openDocumentationBtn = new DzPushButton( quickHelpTab );
openDocumentationBtn.setGeometry( 110, 520, 131, 28 );
openDocumentationBtn.text = "Open Documentation";
openDocumentationBtn.objectName = 'openDocumentationBtn';
connect( openDocumentationBtn, 'clicked()', clicked_openDocumentationBtn );

/*********************************************************************/
function clicked_openDocumentationBtn() {
	
}

// Create and define DzTextEdit: 'helpTextEdit'
var helpTextEdit = new DzTextEdit( quickHelpTab );
helpTextEdit.setGeometry( 10, 170, 331, 301 );

// Create and define DzPushButton: 'createButton'
var createButton = new DzPushButton( Dialog );
createButton.setGeometry( 20, 680, 361, 28 );
createButton.text = "Create billboard(s)";
createButton.objectName = 'createButton';
connect( createButton, 'clicked()', clicked_createButton );

/*********************************************************************/
function clicked_createButton() {
	
}

// Create and define DzPushButton: 'aimButton'
var aimButton = new DzPushButton( Dialog );
aimButton.setGeometry( 20, 650, 181, 28 );
aimButton.text = "Aim Camera";
aimButton.objectName = 'aimButton';
connect( aimButton, 'clicked()', clicked_aimButton );

/*********************************************************************/
function clicked_aimButton() {
	
}

// Create and define DzPushButton: 'frameButton'
var frameButton = new DzPushButton( Dialog );
frameButton.setGeometry( 200, 650, 181, 28 );
frameButton.text = "Frame Camera";
frameButton.objectName = 'frameButton';
connect( frameButton, 'clicked()', clicked_frameButton );

/*********************************************************************/
function clicked_frameButton() {
	
}

// Create button group to manage exclusivity, and for easy reading of which button is selected
var buttonGroup_hardOrSoftBox = new DzButtonGroup( Dialog );
buttonGroup_hardOrSoftBox.setGeometry( 0,0,0,0 );
buttonGroup_hardOrSoftBox.addButton( hardMaskRadio, 0 );
buttonGroup_hardOrSoftBox.addButton( softMaskRadio, 1 );
connect( buttonGroup_hardOrSoftBox, 'pressed( int )', handleExclusivity_buttonGroup_hardOrSoftBox );

// Create button group to manage exclusivity, and for easy reading of which button is selected
var buttonGroup_modeBox = new DzButtonGroup( Dialog );
buttonGroup_modeBox.setGeometry( 0,0,0,0 );
buttonGroup_modeBox.addButton( performanceRadio, 2 );
buttonGroup_modeBox.addButton( preserveRadio, 3 );
connect( buttonGroup_modeBox, 'pressed( int )', handleExclusivity_buttonGroup_modeBox );

/*********************************************************************/
// Function to handle radio button exclusivity for button group: buttonGroup_hardOrSoftBox
function handleExclusivity_buttonGroup_hardOrSoftBox( nBtnID ) {
	switch( nBtnID ) {
		case 0:
			softMaskRadio.checked = false;
			break;
		case 1:
			hardMaskRadio.checked = false;
			break;
		default:
			print( 'Unpexpected radio button ID.' );
	}
}

/*********************************************************************/
// Function to handle radio button exclusivity for button group: buttonGroup_modeBox
function handleExclusivity_buttonGroup_modeBox( nBtnID ) {
	switch( nBtnID ) {
		case 2:
			preserveRadio.checked = false;
			break;
		case 3:
			performanceRadio.checked = false;
			break;
		default:
			print( 'Unpexpected radio button ID.' );
	}
}

// Display the dialog box
var bResult = Dialog.exec();
if( bResult ) {
	// Do if dialog box was accepted
} else {
	// Do if dialog box was canceled
}
