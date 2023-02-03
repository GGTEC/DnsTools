
eel.expose(toast_notifc);
function toast_notifc(text){

  if (text == 'error'){
    text = 'Ocorreu um erro no salvamento, verifique se os dados estão corretos ou entre em contato com o suporte.'
  } else if (text == 'success') {
    text = 'Sucesso ao salvar'
  }

  Bs5Utils.defaults.toasts.position = 'bottom-right';
  Bs5Utils.defaults.toasts.container = 'toast-container';
  Bs5Utils.defaults.toasts.stacking = true;

  const bs5Utils = new Bs5Utils();

  Bs5Utils.registerStyle('dark-purple', {
    btnClose: ['btn-close-white'],
    main: ['bg-dark', 'text-white'],
    border: ['custom-border-modal']
  });

  bs5Utils.Toast.show({
    type: 'dark-purple',
    icon: `<i class="far fa-check-circle fa-lg me-2"></i>`,
    title: 'Notificação',
    subtitle: '',
    buttons : [],
    content: text,
    delay: 5000,
    dismissible: true
});

}

async function get_adapters(inputid) {

    $("#" + inputid).empty();
    input_adapter = document.getElementById(inputid);

    var adapter = await eel.get_adapter_py()();

    if (adapter) {
        input_adapter.value = adapter;
    }
}

function set_dns(){


    input_adapter = document.getElementById('adapter');
    select_dns = document.getElementById('select-dns');

    dns = select_dns.value;
    adapter = input_adapter.value;

    eel.change_dns(adapter,dns)
}
    