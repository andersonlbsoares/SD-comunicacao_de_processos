package questao_01;

import java.io.BufferedWriter;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.io.Writer;
import java.net.Socket;

import questao_01.entidades.Pessoa;

public class PessoasOutputStream extends OutputStream {
	
	private OutputStream op;
	private Pessoa[] pessoas;
	
	public PessoasOutputStream() {}
	
	public PessoasOutputStream(Pessoa[] p, OutputStream os) {
		this.pessoas = p;
		this.op = os;
	}

	public void testaroCodigoNaSaidaConsole() {
		
		PrintStream opLocal = new PrintStream(op);
		//envia quantidade de pessoas;
		int qtdpessoa = pessoas.length;
		opLocal.println("\n"+"Quantidade de pessoas: "+qtdpessoa+"\n"+"------------------"+"\n"+"\n");
		
		//envia os dados de um conjunto (array) de Pessoas
		for (Pessoa pessoa : pessoas) {
			if (pessoa != null) {
				double tamanhoNomePessoa = pessoa.getNome().getBytes().length;
				String nome = pessoa.getNome();
				double cpf = pessoa.getCpf();
				int idade = pessoa.getIdade();
							
				opLocal.println(" tamanhoNomePessoa: "+tamanhoNomePessoa+ "\n"+
								" nomePessoa: "+nome+ "\n"+
								" cpf: "+cpf+ "\n"+
								" idade: "+idade+"\n"+"\n"+"------------------"+"\n"+"\n");
			}
		}
	}


	public void testaroCodigoNaSaidaComoArquivo() {
		for (Pessoa pessoa : pessoas) {
			if (pessoa != null) {
				double tamanhoNomePessoa = pessoa.getNome().getBytes().length;
				String nome = pessoa.getNome();
				double cpf = pessoa.getCpf();
				int idade = pessoa.getIdade();

				try (Writer writer = new BufferedWriter(new OutputStreamWriter(
						new FileOutputStream("FileOutputStream.txt", true), "utf-8"))) {
					writer.write(" tamanhoNomePessoa: "+tamanhoNomePessoa+ "\n"+
							" nomePessoa: "+nome+ "\n"+
							" cpf: "+cpf+ "\n"+
							" idade: "+idade+"\n"+"\n"+"------------------"+"\n"+"\n");
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}

	public void testaroCodigoNaEmConexaoTCP() {
		try {
			Socket socket = new Socket("localhost", 12345); // Conecta ao servidor na porta 12345 (você pode alterar a porta se desejar).
	
			OutputStream os = socket.getOutputStream();
			PrintWriter out = new PrintWriter(os, true);
	
			// Envia a quantidade de pessoas
			int qtdpessoa = pessoas.length;
			out.println("Quantidade de pessoas: " + qtdpessoa);
			out.println("------------------");
	
			// Envia os dados de um conjunto (array) de Pessoas
			for (Pessoa pessoa : pessoas) {
				if (pessoa != null) {
					double tamanhoNomePessoa = pessoa.getNome().getBytes().length;
					String nome = pessoa.getNome();
					double cpf = pessoa.getCpf();
					int idade = pessoa.getIdade();
	
					out.println("tamanhoNomePessoa: " + tamanhoNomePessoa);
					out.println("nomePessoa: " + nome);
					out.println("cpf: " + cpf);
					out.println("idade: " + idade);
					out.println("------------------");
				}
			}
	
			socket.close(); // Fecha a conexão com o servidor.
	
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	@Override
	public void write(int b) throws IOException {
	}

	@Override
	public String toString() {
		return 
				" PessoasOutputStream [ \n"
				+ " getClass()=" + getClass() +",\n"
				+ " hashCode()=" + hashCode() +",\n"
				+ " toString()="+ super.toString() + "]";
	}

	public static void main(String[] args) {
        
        Pessoa[] pessoas = new Pessoa[3];
        pessoas[0] = new Pessoa("Joao", 123456789, 20);
        pessoas[1] = new Pessoa("Maria", 987654321, 30);
        pessoas[2] = new Pessoa("Jose", 123456789, 40);
        
		//testaroCodigoNaSaidaConsole
		PessoasOutputStream pos = new PessoasOutputStream(pessoas, System.out);
		
		//testaroCodigoNaSaidaConsole();
		pos.testaroCodigoNaSaidaConsole();
		
		// testaroCodigoNaSaidaComoArquivo
		pos.testaroCodigoNaSaidaComoArquivo();

		// testaroCodigoNaEmConexaoTCP
		pos.testaroCodigoNaEmConexaoTCP();


		//agora testa usando o TCP



	}
}


