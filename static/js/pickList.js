(function ($) {

   $.fn.pickList = function (options) {

      var opts = $.extend({}, $.fn.pickList.defaults, options);

      this.fill = function () {
         var option = '';
         var optionSelect = '';

         $.each(opts.data, function (id,val) {
            if(val.isSel ==1){
               optionSelect += '<option data-id=' + val.id + '>' + val.text + '</option>';
            }
            else {
               option += '<option data-id=' + val.id + '>' + val.text + '</option>';
            }
         });
         this.find('.pickData').append(option);
         this.find('.pickListResult').append(optionSelect);
      };
      this.controll = function () {
         var pickThis = this;

         pickThis.find(".pAdd").on('click', function () {
            var p = pickThis.find(".pickData option:selected");
            p.clone().appendTo(pickThis.find(".pickListResult"));
            p.remove();
         });

         pickThis.find(".pAddAll").on('click', function () {
            var p = pickThis.find(".pickData option");
            p.clone().appendTo(pickThis.find(".pickListResult"));
            p.remove();
         });

         pickThis.find(".pRemove").on('click', function () {
            var p = pickThis.find(".pickListResult option:selected");
            p.clone().appendTo(pickThis.find(".pickData"));
            p.remove();
         });

         pickThis.find(".pRemoveAll").on('click', function () {
            var p = pickThis.find(".pickListResult option");
            p.clone().appendTo(pickThis.find(".pickData"));
            p.remove();
         });
      };

      this.getValues = function () {
         var objResult = [];
         this.find(".pickListResult option").each(function () {
            objResult.push({
               id: $(this).data('id'),
               text: this.text
            });
         });
         return objResult;
      };

      this.init = function () {
         var pickListHtml =
                 "<div class='pickRow'>" +
                 "  <div class='col-sm-5'>" +
                 "	 <select class='form-control pickListSelect pickData' multiple></select>" +
                 " </div>" +
                 " <div class='col-sm-2 pickListButtons'>" +
                 "	<a  class='pAdd btn btn-default'>" + opts.add + "</a><br>" +
                 "      <a  class='pAddAll btn btn-default'>" + opts.addAll + "</a><br>" +
                 "	<a  class='pRemove btn btn-default'>" + opts.remove + "</a><br>" +
                 "	<a  class='pRemoveAll btn btn-default'>" + opts.removeAll + "</a><br>" +
                 " </div>" +
                 " <div class='col-sm-4'>" +
                 "    <select class='form-control pickListSelect pickListResult' multiple></select>" +
                 " </div>" +
                 "</div>";

         this.append(pickListHtml);

         this.fill();
         this.controll();
      };

      this.init();
      return this;
   };

   $.fn.pickList.defaults = {
      add: '添加',
      addAll: '添加全部',
      remove: '删除',
      removeAll: '删除全部'
   };


}(jQuery));
