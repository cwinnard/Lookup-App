$(document).ready(function() {
	//Event listeners for hide/show functionality
	$('#collapseContacts').on('click', _hideContacts);
	$('#expandContacts').on('click', _showContacts);
	$('#collapseManage').on('click', _hideManage);
	$('#expandManage').on('click', _showManage);
	
	function _hideContacts() {
		$('.contact').hide();
		$('#collapseContacts').hide();
		$('#expandContacts').show();
	}
	
	function _showContacts() {
		$('.contact').show();
		$('#collapseContacts').show();
		$('#expandContacts').hide();
	}
	
	function _hideManage() {
		$('.lookupWrapper').hide();
		$('.addContact').hide();
		$('.deleteContact').hide();
		$('#collapseManage').hide();
		$('#expandManage').show();
	}
	
	function _showManage() {
		$('.lookupWrapper').show();
		$('.addContact').show();
		$('.deleteContact').show();
		$('#collapseManage').show();
		$('#expandManage').hide();
	}
	
	//Event listeners for question tooltip functionality
	$('#infoContacts').on('click', _showContactsModal);
	$('#infoManage').on('click', _showManageModal);
	$('.close').on('click', _closeModal);
	
	function _showContactsModal() {
		$('#modalContacts').show();
	}
	
	function _showManageModal() {
		$('#modalManage').show();
	}
	
	function _closeModal(){
		$('#modalContacts').hide();
		$('#modalManage').hide();
	}
})