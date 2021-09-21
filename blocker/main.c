#include <gtk/gtk.h>

gboolean my_keypress_function (GtkWidget *widget, GdkEventKey *event, gpointer data) {
    if (event->keyval == GDK_KEY_Escape){
        printf("ESC KEY PRESSED!");
	exit(0);
        return TRUE;
    }
    return FALSE;
}


static void
activate (GtkApplication* app,
          gpointer        user_data)
{
  GtkWidget *window;

  window = gtk_application_window_new (app);
  gtk_window_set_title (GTK_WINDOW (window), "Window");
  gtk_window_move (GTK_WINDOW (window),0,0);
  gtk_window_set_default_size (GTK_WINDOW (window), 3840, 1080);
  gtk_window_set_decorated(GTK_WINDOW (window), FALSE);

  GdkColor color;
  color.red = 0x00C0;
  color.green = 0x00DE;
  color.blue = 0x00ED;
  gtk_widget_modify_bg(GTK_WINDOW(window), GTK_STATE_NORMAL, &color);


  g_signal_connect (G_OBJECT (window), "key_press_event",
        G_CALLBACK (my_keypress_function), NULL);

  gtk_widget_show_all (window);
  //gtk_window_set_screen (GTK_WINDOW (window), (int)user_data);
}

int
main (int    argc,
      char **argv)
{
  GtkApplication *app;
  int status;

  app = gtk_application_new ("org.gtk.example", G_APPLICATION_FLAGS_NONE);
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
  status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (app);

  return status;
}
